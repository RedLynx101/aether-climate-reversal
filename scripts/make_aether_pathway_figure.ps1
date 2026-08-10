$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$Table = Join-Path $Root "analysis\tables\aether_pathway_portfolio_allocation.csv"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null
$OutPath = Join-Path $FigureDir "pathway_portfolio_100gt.png"

function Save-Png($Bitmap, [string]$Path) {
    $ms = New-Object System.IO.MemoryStream
    $Bitmap.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
    [System.IO.File]::WriteAllBytes($Path, $ms.ToArray())
    $ms.Dispose()
}

$rows = @(Import-Csv $Table | Sort-Object {[double]$_.aether_optimized_allocation_gtco2_y} -Descending)
$width = 1500
$height = 920
$bmp = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(250,250,248))

$titleFont = New-Object System.Drawing.Font("Arial", 30, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 15)
$labelFont = New-Object System.Drawing.Font("Arial", 14)
$valueFont = New-Object System.Drawing.Font("Arial", 13, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Arial", 11)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(95,95,95), 2)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(225,225,220), 1)
$barBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(42, 104, 130))
$assessmentBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(176, 188, 191))

$g.DrawString("AETHER 100 GtCO2/year Pathway Portfolio", $titleFont, [System.Drawing.Brushes]::Black, 70, 42)
$g.DrawString("Optimized allocation assumptions compared with central assessed potential ranges.", $subFont, [System.Drawing.Brushes]::DimGray, 72, 88)

$displayLabels = @{
    "daccs_geologic" = "DACCS + geologic storage"
    "enhanced_weathering" = "Enhanced weathering"
    "ocean_alkalinity_enhancement" = "Ocean alkalinity"
    "beccs" = "BECCS"
    "biochar" = "Biochar"
    "afforestation_reforestation" = "Afforestation/reforestation"
    "direct_ocean_capture" = "Direct ocean capture"
}

$left = 430
$top = 150
$barH = 42
$gap = 31
$maxW = 760
$maxValue = 45.0

for ($i = 0; $i -le 4; $i++) {
    $x = $left + ($maxW * $i / 4)
    $g.DrawLine($gridPen, $x, $top - 18, $x, $top + ($barH + $gap) * $rows.Count - $gap + 8)
    $tick = [int]($maxValue * $i / 4)
    $g.DrawString([string]$tick, $labelFont, [System.Drawing.Brushes]::DimGray, $x - 8, $top + ($barH + $gap) * $rows.Count + 3)
}
$g.DrawLine($axisPen, $left, $top - 18, $left, $top + ($barH + $gap) * $rows.Count - $gap + 8)

for ($i = 0; $i -lt $rows.Count; $i++) {
    $r = $rows[$i]
    $y = $top + $i * ($barH + $gap)
    $allocation = [double]$r.aether_optimized_allocation_gtco2_y
    $assessed = [double]$r.assessed_central_potential_gtco2_y
    $allocationW = $maxW * $allocation / $maxValue
    $assessedW = $maxW * $assessed / $maxValue
    $display = $displayLabels[$r.pathway]
    if (-not $display) {
        $display = [string]$r.display_name
    }
    $g.DrawString($display, $labelFont, [System.Drawing.Brushes]::Black, 70, $y + 9)
    $g.FillRectangle($assessmentBrush, $left, $y + 8, [float]$assessedW, 12)
    $g.FillRectangle($barBrush, $left, $y + 22, [float]$allocationW, 18)
    $label = $allocation.ToString("0.#") + " Gt/y; $" + ([double]$r.aether_optimized_cost_usd_tco2_assumption).ToString("0") + "/t"
    $g.DrawString($label, $valueFont, [System.Drawing.Brushes]::Black, [float]($left + $allocationW + 14), $y + 17)
}

$legendFont = New-Object System.Drawing.Font("Arial", 12)
$legendY = 782
$g.FillRectangle($barBrush, 72, $legendY, 28, 14)
$g.DrawString("AETHER optimized allocation", $legendFont, [System.Drawing.Brushes]::Black, 110, $legendY - 4)
$g.FillRectangle($assessmentBrush, 350, $legendY, 28, 14)
$g.DrawString("Central assessed potential", $legendFont, [System.Drawing.Brushes]::Black, 388, $legendY - 4)
$g.DrawString("GtCO2/year", $labelFont, [System.Drawing.Brushes]::DimGray, $left + $maxW - 65, $top + ($barH + $gap) * $rows.Count + 35)
$g.DrawString("Source: aether_pathway_portfolio_model.py; IPCC AR6 WGIII TS.7 and NASEM ocean CDR report.", $footerFont, [System.Drawing.Brushes]::DimGray, 70, $height - 46)

Save-Png $bmp $OutPath

$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $valueFont.Dispose(); $footerFont.Dispose(); $legendFont.Dispose()
$axisPen.Dispose(); $gridPen.Dispose(); $barBrush.Dispose(); $assessmentBrush.Dispose(); $g.Dispose(); $bmp.Dispose()
Get-Item $OutPath | Select-Object FullName,Length
