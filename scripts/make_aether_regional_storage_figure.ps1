$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$TableDir = Join-Path $Root "analysis\tables"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null

function Save-Png($Bitmap, [string]$Path) {
    $ms = New-Object System.IO.MemoryStream
    $Bitmap.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
    [System.IO.File]::WriteAllBytes($Path, $ms.ToArray())
    $ms.Dispose()
}

function Format-CompactNumber([double]$Value) {
    if ($Value -ge 1000) {
        return ($Value / 1000.0).ToString("0.#") + "k"
    }
    return $Value.ToString("0")
}

function Draw-WrappedText($Graphics, [string]$Text, $Font, $Brush, [float]$X, [float]$Y, [float]$Width, [float]$LineHeight) {
    $words = $Text -split "\s+"
    $line = ""
    foreach ($word in $words) {
        $candidate = if ([string]::IsNullOrWhiteSpace($line)) { $word } else { $line + " " + $word }
        if ($Graphics.MeasureString($candidate, $Font).Width -le $Width) {
            $line = $candidate
        } else {
            if (-not [string]::IsNullOrWhiteSpace($line)) {
                $Graphics.DrawString($line, $Font, $Brush, $X, $Y)
                $Y += $LineHeight
            }
            $line = $word
        }
    }
    if (-not [string]::IsNullOrWhiteSpace($line)) {
        $Graphics.DrawString($line, $Font, $Brush, $X, $Y)
        $Y += $LineHeight
    }
    return $Y
}

$allocation = @(Import-Csv (Join-Path $TableDir "aether_regional_storage_allocation.csv") | Sort-Object {[double]$_.assigned_injection_gtco2_y} -Descending)
$corridors = @(Import-Csv (Join-Path $TableDir "aether_injection_corridor_requirements.csv"))

$caseRows = @()
foreach ($productivity in @(0.25, 0.5, 1.0, 2.0)) {
    $caseRows += [pscustomobject]@{
        productivity = $productivity
        wells = (($corridors | Where-Object {[double]$_.well_productivity_mtco2_y -eq $productivity} | Measure-Object -Property required_injection_wells -Sum).Sum)
    }
}

$width = 1600
$height = 1000
$bmp = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(250,250,248))

$titleFont = New-Object System.Drawing.Font("Arial", 29, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 15)
$labelFont = New-Object System.Drawing.Font("Arial", 12)
$boldFont = New-Object System.Drawing.Font("Arial", 12, [System.Drawing.FontStyle]::Bold)
$smallFont = New-Object System.Drawing.Font("Arial", 10)
$footerFont = New-Object System.Drawing.Font("Arial", 10)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(224,224,218), 1)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(92,92,88), 2)
$assignBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(43, 105, 127))
$placeholderBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(195, 137, 68))
$wellBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(108, 133, 95))

$g.DrawString("AETHER Regional Storage and Injection Corridors", $titleFont, [System.Drawing.Brushes]::Black, 62, 38)
$g.DrawString("First screen for assigning 54 GtCO2/year of geologic storage throughput to regional corridors.", $subFont, [System.Drawing.Brushes]::DimGray, 64, 84)

$left = 460
$top = 145
$barH = 31
$gap = 27
$maxW = 610
$maxAssigned = 18.0

$g.DrawString("Regional allocation screen", $boldFont, [System.Drawing.Brushes]::Black, 64, 120)
for ($i = 0; $i -le 3; $i++) {
    $x = $left + $maxW * $i / 3
    $g.DrawLine($gridPen, $x, $top - 10, $x, $top + ($barH + $gap) * $allocation.Count - $gap + 15)
    $g.DrawString((($maxAssigned * $i / 3).ToString("0") + " Gt/y"), $smallFont, [System.Drawing.Brushes]::DimGray, $x - 20, $top + ($barH + $gap) * $allocation.Count - 2)
}
$g.DrawLine($axisPen, $left, $top - 10, $left, $top + ($barH + $gap) * $allocation.Count - $gap + 15)

for ($i = 0; $i -lt $allocation.Count; $i++) {
    $r = $allocation[$i]
    $y = $top + $i * ($barH + $gap)
    $assigned = [double]$r.assigned_injection_gtco2_y
    $w = $maxW * $assigned / $maxAssigned
    $brush = if ($r.evidence_class.StartsWith("source-backed")) { $assignBrush } else { $placeholderBrush }
    $g.DrawString($r.region_name, $boldFont, [System.Drawing.Brushes]::Black, 64, $y + 5)
    $g.FillRectangle($brush, $left, $y + 3, [float]$w, $barH)
    $label = $assigned.ToString("0.#") + " Gt/y; " + ([double]$r.capacity_years_at_assigned_rate).ToString("0") + " years proxy"
    $g.DrawString($label, $labelFont, [System.Drawing.Brushes]::Black, [float]($left + $w + 12), $y + 7)
}

$legendY = 566
$g.FillRectangle($assignBrush, 64, $legendY, 24, 13)
$g.DrawString("Source-backed U.S. anchor", $smallFont, [System.Drawing.Brushes]::Black, 96, $legendY - 3)
$g.FillRectangle($placeholderBrush, 300, $legendY, 24, 13)
$g.DrawString("Scenario placeholder", $smallFont, [System.Drawing.Brushes]::Black, 332, $legendY - 3)

$caseTop = 650
$caseLeft = 460
$caseMaxW = 760
$caseMax = (($caseRows | Measure-Object -Property wells -Maximum).Maximum)
$g.DrawString("Pressure-adjusted injection-well requirements", $boldFont, [System.Drawing.Brushes]::Black, 64, $caseTop - 42)
$g.DrawString("One permit/well in the U.S. Class VI frame; non-U.S. rows need country-specific permitting models.", $smallFont, [System.Drawing.Brushes]::DimGray, 64, $caseTop - 20)
for ($i = 0; $i -lt $caseRows.Count; $i++) {
    $r = $caseRows[$i]
    $y = $caseTop + $i * 55
    $w = $caseMaxW * $r.wells / $caseMax
    $g.DrawString($r.productivity.ToString("0.##") + " MtCO2/well-y", $boldFont, [System.Drawing.Brushes]::Black, 64, $y + 8)
    $g.FillRectangle($wellBrush, $caseLeft, $y + 5, [float]$w, 33)
    $g.DrawString((Format-CompactNumber $r.wells) + " wells", $labelFont, [System.Drawing.Brushes]::Black, [float]($caseLeft + $w + 12), $y + 10)
}

$calloutX = 1110
$calloutY = 154
$calloutFont = New-Object System.Drawing.Font("Arial", 13)
$calloutBold = New-Object System.Drawing.Font("Arial", 14, [System.Drawing.FontStyle]::Bold)
$g.DrawString("Main read", $calloutBold, [System.Drawing.Brushes]::Black, $calloutX, $calloutY)
$calloutY += 36
$callouts = @(
    "Storage resource is not the same as injection rate.",
    "USGS gives a strong U.S. capacity anchor, especially the Gulf Coast.",
    "The model still needs basin-level permeability, pressure, and brine data.",
    "EPA Class VI turns each U.S. well into a permit and monitoring object.",
    "AETHER-scale storage is a corridor program, not a single sink."
)
foreach ($text in $callouts) {
    $calloutY = Draw-WrappedText $g $text $calloutFont ([System.Drawing.Brushes]::DimGray) $calloutX $calloutY 410 22
    $calloutY += 12
}

$g.DrawString("Source: aether_regional_storage_injection_model.py. U.S. capacity anchored to USGS Circular 1386; regulatory frame anchored to EPA Class VI pages.", $footerFont, [System.Drawing.Brushes]::DimGray, 64, $height - 45)
Save-Png $bmp (Join-Path $FigureDir "regional_storage_injection_corridors.png")

$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $smallFont.Dispose(); $footerFont.Dispose()
$gridPen.Dispose(); $axisPen.Dispose(); $assignBrush.Dispose(); $placeholderBrush.Dispose(); $wellBrush.Dispose(); $calloutFont.Dispose(); $calloutBold.Dispose()
$g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "regional_storage_injection_corridors.png") | Select-Object FullName,Length

