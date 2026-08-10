$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$TableDir = Join-Path $Root "analysis\tables"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null

function Save-Png {
    param([Parameter(Mandatory = $true)][System.Drawing.Bitmap]$Bitmap, [Parameter(Mandatory = $true)][string]$Path)
    if (Test-Path -LiteralPath $Path) { Remove-Item -LiteralPath $Path -Force }
    $Bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
}

$rows = @(Import-Csv (Join-Path $TableDir "aether_pathway_source_gap_analysis.csv") | Where-Object { $_.plot_include -eq "true" })

$width = 1600
$height = 980
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font("Arial", 25, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 14)
$labelFont = New-Object System.Drawing.Font("Arial", 11)
$boldFont = New-Object System.Drawing.Font("Arial", 11, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Consolas", 9)

$g.DrawString("AETHER Portfolio Against Assessed CDR Potential Ranges", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("Orange markers show the current AETHER 100 GtCO2/year allocation; gray bars show source-assessed annual potential ranges.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 430
$top = 150
$maxW = 840
$barH = 34
$gap = 78
$max = 100.0
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(120,120,120), 1)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)
$fullBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(220, 224, 224))
$centralBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(112, 132, 145))
$markerPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(210, 111, 48), 5)

for ($tick = 0; $tick -le 100; $tick += 20) {
    $x = $left + $maxW * $tick / $max
    $g.DrawLine($gridPen, [float]$x, $top - 24, [float]$x, $top + ($barH + $gap) * $rows.Count - 32)
    $g.DrawString($tick.ToString() + " Gt/y", $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 18), $top + ($barH + $gap) * $rows.Count - 14)
}
$g.DrawLine($axisPen, $left, $top - 24, $left, $top + ($barH + $gap) * $rows.Count - 32)

for ($i = 0; $i -lt $rows.Count; $i++) {
    $row = $rows[$i]
    $y = $top + $i * ($barH + $gap)
    $allocation = [double]$row.aether_allocation_gtco2_y
    $centralHigh = [double]$row.potential_high_gtco2_y
    $fullHigh = [double]$row.potential_full_high_gtco2_y
    $fullW = $maxW * [Math]::Min($fullHigh, $max) / $max
    $centralW = $maxW * [Math]::Min($centralHigh, $max) / $max
    $markerX = $left + $maxW * [Math]::Min($allocation, $max) / $max

    $g.DrawString($row.display_name, $boldFont, [System.Drawing.Brushes]::Black, 66, $y - 4)
    $g.DrawString($row.classification, $labelFont, [System.Drawing.Brushes]::DimGray, 66, $y + 22)
    $g.FillRectangle($fullBrush, $left, $y, [float]$fullW, $barH)
    $g.FillRectangle($centralBrush, $left, $y + 6, [float]$centralW, $barH - 12)
    $g.DrawLine($markerPen, [float]$markerX, $y - 5, [float]$markerX, $y + $barH + 5)
    $g.DrawString("AETHER " + $allocation.ToString("0.#") + " Gt/y; assessed high " + $centralHigh.ToString("0.#") + " Gt/y", $labelFont, [System.Drawing.Brushes]::Black, [float]($left + [Math]::Max($centralW, $markerX - $left) + 16), $y + 8)
}

$legendY = 855
$g.FillRectangle($centralBrush, 66, $legendY, 32, 14)
$g.DrawString("IPCC assessed range high", $labelFont, [System.Drawing.Brushes]::Black, 106, $legendY - 4)
$g.FillRectangle($fullBrush, 340, $legendY, 32, 14)
$g.DrawString("Full literature range high where reported", $labelFont, [System.Drawing.Brushes]::Black, 380, $legendY - 4)
$g.DrawLine($markerPen, 660, $legendY - 4, 660, $legendY + 20)
$g.DrawString("AETHER allocation", $labelFont, [System.Drawing.Brushes]::Black, 678, $legendY - 4)
$g.DrawString("Source: aether_cdr_pathway_source_ranges.csv; IPCC AR6 WGIII Table TS.7 plus NASEM ocean CDR caution.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 45)

Save-Png $bmp (Join-Path $FigureDir "pathway_source_ranges_vs_aether.png")
$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$axisPen.Dispose(); $gridPen.Dispose(); $fullBrush.Dispose(); $centralBrush.Dispose(); $markerPen.Dispose()
$g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "pathway_source_ranges_vs_aether.png") | Select-Object FullName,Length

