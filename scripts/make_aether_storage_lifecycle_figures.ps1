$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$RoutesTable = Join-Path $Root "analysis\tables\aether_storage_lifecycle_routes.csv"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null

function Save-Png($Bitmap, [string]$Path) {
    $ms = New-Object System.IO.MemoryStream
    $Bitmap.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
    [System.IO.File]::WriteAllBytes($Path, $ms.ToArray())
    $ms.Dispose()
}

$rows = @(Import-Csv $RoutesTable | Sort-Object {[double]$_.gross_allocation_gtco2_y} -Descending)
$displayLabels = @{
    "daccs_geologic" = "DACCS"
    "enhanced_weathering" = "Enhanced weathering"
    "ocean_alkalinity_enhancement" = "Ocean alkalinity"
    "beccs" = "BECCS"
    "biochar" = "Biochar"
    "afforestation_reforestation" = "Afforestation"
    "direct_ocean_capture" = "Direct ocean capture"
}

$width = 1500
$height = 930
$bmp = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(250,250,248))

$titleFont = New-Object System.Drawing.Font("Arial", 29, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 15)
$labelFont = New-Object System.Drawing.Font("Arial", 13)
$boldFont = New-Object System.Drawing.Font("Arial", 13, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Arial", 10)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(224,224,218), 1)
$grossBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(49, 105, 132))
$durableBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(91, 143, 107))

$g.DrawString("AETHER Storage and Lifecycle Durability Filter", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("Gross pathway allocation compared with 100-year durable credited removal after lifecycle and reversal haircuts.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 380
$top = 152
$barH = 34
$gap = 42
$maxW = 760
$maxValue = 45.0

for ($i = 0; $i -le 5; $i++) {
    $x = $left + $maxW * $i / 5
    $g.DrawLine($gridPen, $x, $top - 16, $x, $top + ($barH + $gap) * $rows.Count - $gap + 30)
    $tick = [int]($maxValue * $i / 5)
    $g.DrawString([string]$tick, $labelFont, [System.Drawing.Brushes]::DimGray, $x - 10, $top + ($barH + $gap) * $rows.Count + 2)
}

for ($i = 0; $i -lt $rows.Count; $i++) {
    $r = $rows[$i]
    $y = $top + $i * ($barH + $gap)
    $gross = [double]$r.gross_allocation_gtco2_y
    $durable = [double]$r.durable_100y_credit_gtco2_y
    $grossW = $maxW * $gross / $maxValue
    $durableW = $maxW * $durable / $maxValue
    $label = $displayLabels[$r.pathway]
    $g.DrawString($label, $boldFont, [System.Drawing.Brushes]::Black, 66, $y + 10)
    $g.FillRectangle($grossBrush, $left, $y + 2, [float]$grossW, 16)
    $g.FillRectangle($durableBrush, $left, $y + 22, [float]$durableW, 16)
    $value = $durable.ToString("0.0") + " net of " + $gross.ToString("0.#") + " Gt/y"
    $g.DrawString($value, $labelFont, [System.Drawing.Brushes]::Black, [float]($left + [Math]::Max($grossW, $durableW) + 14), $y + 13)
}

$legendY = 735
$g.FillRectangle($grossBrush, 66, $legendY, 28, 14)
$g.DrawString("Gross allocation", $labelFont, [System.Drawing.Brushes]::Black, 104, $legendY - 4)
$g.FillRectangle($durableBrush, 260, $legendY, 28, 14)
$g.DrawString("Durable credited removal after 100 years", $labelFont, [System.Drawing.Brushes]::Black, 298, $legendY - 4)
$g.DrawString("GtCO2/year", $labelFont, [System.Drawing.Brushes]::DimGray, $left + $maxW - 60, $top + ($barH + $gap) * $rows.Count + 34)
$g.DrawString("Source: aether_storage_lifecycle_model.py; route haircuts are explicit AETHER assumptions anchored to USGS/IPCC/NASEM storage constraints.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 45)
Save-Png $bmp (Join-Path $FigureDir "storage_lifecycle_net_durable_100y.png")

$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$gridPen.Dispose(); $grossBrush.Dispose(); $durableBrush.Dispose(); $g.Dispose(); $bmp.Dispose()

$bmp = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(250,250,248))
$titleFont = New-Object System.Drawing.Font("Arial", 29, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 15)
$labelFont = New-Object System.Drawing.Font("Arial", 12)
$boldFont = New-Object System.Drawing.Font("Arial", 12, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Arial", 10)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(90,90,85), 2)
$barBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(202, 138, 66))

$g.DrawString("Storage Scale: Injection and Processing Burden", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("One-Mt/year well equivalents for geologic routes; non-geologic routes shown as ten-Mt/year processing hubs.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 430
$top = 150
$barH = 36
$gap = 42
$maxW = 800
$maxValue = 45000.0

for ($i = 0; $i -lt $rows.Count; $i++) {
    $r = $rows[$i]
    $y = $top + $i * ($barH + $gap)
    $label = $displayLabels[$r.pathway]
    $burden = if ([double]$r.one_mt_injection_well_equivalents -gt 0) { [double]$r.one_mt_injection_well_equivalents } else { [double]$r.ten_mt_hub_equivalents }
    $suffix = if ([double]$r.one_mt_injection_well_equivalents -gt 0) { " one-Mt/y injection wells" } else { " ten-Mt/y processing hubs" }
    $w = $maxW * $burden / $maxValue
    $g.DrawString($label, $boldFont, [System.Drawing.Brushes]::Black, 66, $y + 8)
    $g.FillRectangle($barBrush, $left, $y + 7, [float]$w, $barH - 10)
    $g.DrawString($burden.ToString("0,0") + $suffix, $labelFont, [System.Drawing.Brushes]::Black, [float]($left + $w + 14), $y + 9)
}
$g.DrawLine($axisPen, $left, $top - 10, $left, $top + ($barH + $gap) * $rows.Count - $gap + 10)
$g.DrawString("This is a deployment-burden proxy, not a well design. Real injection depends on reservoir pressure, permeability, brine handling, monitoring, and permitting.", $labelFont, [System.Drawing.Brushes]::DimGray, 66, 765)
$g.DrawString("Source: aether_storage_lifecycle_model.py; IPCC AR6 WGIII notes pressure can limit injection even where storage resource is large.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 45)
Save-Png $bmp (Join-Path $FigureDir "storage_injection_processing_burden.png")

$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$axisPen.Dispose(); $barBrush.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "storage_lifecycle_net_durable_100y.png"), (Join-Path $FigureDir "storage_injection_processing_burden.png") | Select-Object FullName,Length
