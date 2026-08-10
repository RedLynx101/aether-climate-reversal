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

$frontier = @(Import-Csv (Join-Path $TableDir "aether_cost_improvement_frontier.csv") | Where-Object { $_.scenario -ne "splitting_default_failure" })
$buckets = @(Import-Csv (Join-Path $TableDir "aether_cost_bucket_reduction_factors.csv") | Where-Object { $_.target_scenario -eq "deep_abundance_floor" -and $_.component -ne "product_handling" })

$width = 1700
$height = 1240
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font("Arial", 26, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 14)
$sectionFont = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
$labelFont = New-Object System.Drawing.Font("Arial", 10)
$boldFont = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Consolas", 9)

$blueBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(65, 125, 145))
$orangeBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(205, 117, 45))
$greenBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(83, 139, 94))
$grayBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::DimGray)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)

$g.DrawString("AETHER Technology Acceleration Frontier", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("The optimistic case is not one miracle. It is a coupled reduction across energy, plants, materials, robots, MRV, finance, and storage.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 450
$top = 165
$maxW = 920
$barH = 38
$gap = 58
$g.DrawString("Delivered cost frontier at 100 GtCO2/year", $sectionFont, [System.Drawing.Brushes]::Black, 66, $top - 48)
for ($tick = 0; $tick -le 600; $tick += 100) {
    $x = $left + $maxW * $tick / 650.0
    $g.DrawLine($gridPen, [float]$x, $top - 8, [float]$x, $top + ($barH + $gap) * $frontier.Count - $gap + 10)
    $g.DrawString(("$" + $tick), $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 12), $top + ($barH + $gap) * $frontier.Count - 20)
}
for ($i = 0; $i -lt $frontier.Count; $i++) {
    $row = $frontier[$i]
    $y = $top + $i * ($barH + $gap)
    $cost = [double]$row.delivered_cost_usd_tco2
    $w = [Math]::Max(4, $maxW * $cost / 650.0)
    $brush = if ($row.scenario -eq "current_dac_like") { $blueBrush } elseif ($row.scenario -eq "deep_abundance_floor") { $greenBrush } else { $orangeBrush }
    $g.DrawString($row.display_name, $boldFont, [System.Drawing.Brushes]::Black, 66, $y + 2)
    $g.DrawString(("reduction vs current: {0}x ({1} orders)" -f $row.reduction_factor_vs_current, $row.log10_reduction_orders), $labelFont, [System.Drawing.Brushes]::DimGray, 66, $y + 24)
    $g.FillRectangle($brush, $left, $y, [float]$w, $barH)
    $g.DrawString(("$" + $cost.ToString("N0") + "/tCO2; $" + ([double]$row.annual_cost_trillion_usd_y_at_100gt).ToString("N1") + "T/y"), $boldFont, [System.Drawing.Brushes]::Black, [float]($left + $w + 12), $y + 10)
}

$bucketTop = 610
$g.DrawString("Deep-abundance bucket reductions from current DAC-like stack", $sectionFont, [System.Drawing.Brushes]::Black, 66, $bucketTop - 42)
$bucketLeft = 450
$bucketMaxW = 920
$bucketBarH = 28
$bucketGap = 42
for ($tick = 0; $tick -le 40; $tick += 10) {
    $x = $bucketLeft + $bucketMaxW * $tick / 42.0
    $g.DrawLine($gridPen, [float]$x, $bucketTop - 8, [float]$x, $bucketTop + ($bucketBarH + $bucketGap) * $buckets.Count - $bucketGap + 10)
    $g.DrawString(($tick.ToString() + "x"), $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 10), $bucketTop + ($bucketBarH + $bucketGap) * $buckets.Count - 20)
}
for ($i = 0; $i -lt $buckets.Count; $i++) {
    $row = $buckets[$i]
    $y = $bucketTop + $i * ($bucketBarH + $bucketGap)
    $factor = [double]$row.reduction_factor
    $w = [Math]::Max(4, $bucketMaxW * $factor / 42.0)
    $brush = if ($row.floor_status -like "*hard*") { $blueBrush } elseif ($row.floor_status -like "mostly*") { $greenBrush } else { $orangeBrush }
    $g.DrawString($row.component_label, $boldFont, [System.Drawing.Brushes]::Black, 66, $y)
    $g.DrawString($row.floor_status, $labelFont, [System.Drawing.Brushes]::DimGray, 66, $y + 20)
    $g.FillRectangle($brush, $bucketLeft, $y, [float]$w, $bucketBarH)
    $g.DrawString(($factor.ToString("N1") + "x"), $boldFont, [System.Drawing.Brushes]::Black, [float]($bucketLeft + $w + 12), $y + 5)
}

$legendY = $bucketTop + (($bucketBarH + $bucketGap) * $buckets.Count) + 18
$g.DrawString("Blue buckets retain hard physical or liability floors; green buckets are most directly attacked by robotics and manufacturing; orange are mixed.", $labelFont, [System.Drawing.Brushes]::DimGray, 66, $legendY)
$g.DrawString("Source: aether_cost_improvement_frontier.csv and aether_cost_bucket_reduction_factors.csv.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 42)

Save-Png $bmp (Join-Path $FigureDir "technology_acceleration_frontier.png")
$titleFont.Dispose(); $subFont.Dispose(); $sectionFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$blueBrush.Dispose(); $orangeBrush.Dispose(); $greenBrush.Dispose(); $grayBrush.Dispose(); $gridPen.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "technology_acceleration_frontier.png") | Select-Object FullName,Length
