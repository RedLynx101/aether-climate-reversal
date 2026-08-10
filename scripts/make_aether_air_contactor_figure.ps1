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

$airRows = @(Import-Csv (Join-Path $TableDir "aether_air_contactor_scale.csv") | Where-Object { $_.target_case -eq "full_100gt_all_air" })
$summary = @(Import-Csv (Join-Path $TableDir "aether_air_contactor_scale_summary.csv"))
$sorbentRows = @(Import-Csv (Join-Path $TableDir "aether_sorbent_inventory_scale.csv") | Where-Object { $_.target_case -eq "full_100gt_all_air" })

$scenarioOrder = @(
    "aether_low_pressure_modular",
    "nasem_liquid_contactor_reference",
    "solid_sorbent_mid_pressure",
    "high_pressure_warning"
)
$scenarioLabels = @{
    aether_low_pressure_modular = "AETHER low-pressure"
    nasem_liquid_contactor_reference = "NASEM reference"
    solid_sorbent_mid_pressure = "Solid sorbent mid"
    high_pressure_warning = "High-pressure warning"
}
$colors = @{
    aether_low_pressure_modular = [System.Drawing.Color]::FromArgb(72, 142, 116)
    nasem_liquid_contactor_reference = [System.Drawing.Color]::FromArgb(64, 134, 160)
    solid_sorbent_mid_pressure = [System.Drawing.Color]::FromArgb(218, 150, 62)
    high_pressure_warning = [System.Drawing.Color]::FromArgb(166, 82, 75)
}

$width = 1700
$height = 1060
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font("Arial", 26, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 14)
$sectionFont = New-Object System.Drawing.Font("Arial", 15, [System.Drawing.FontStyle]::Bold)
$labelFont = New-Object System.Drawing.Font("Arial", 10)
$boldFont = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Consolas", 9)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)

$g.DrawString("AETHER Air-Contactor Physical Scale", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("At 100 GtCO2/year, air flow, face area, pressure drop, and sorbent replacement become first-order constraints.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 420
$top = 165
$barH = 54
$gap = 72
$maxArea = 6500.0
$maxW = 940
$g.DrawString("Contactor face area for 100 GtCO2/year all-air capture", $sectionFont, [System.Drawing.Brushes]::Black, 66, 122)
for ($tick = 0; $tick -le 6000; $tick += 1500) {
    $x = $left + $maxW * $tick / $maxArea
    $g.DrawLine($gridPen, [float]$x, $top - 10, [float]$x, $top + ($barH + $gap) * $scenarioOrder.Count - $gap + 30)
    $g.DrawString(($tick.ToString("N0") + " km2"), $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 28), $top + ($barH + $gap) * $scenarioOrder.Count - 20)
}

for ($i = 0; $i -lt $scenarioOrder.Count; $i++) {
    $scenario = $scenarioOrder[$i]
    $row = @($airRows | Where-Object { $_.scenario -eq $scenario })[0]
    $area = [double]$row.contactor_face_area_km2
    $fan = [double]$row.fan_energy_twh_y
    $flow = [double]$row.air_flow_m3_s
    $y = $top + $i * ($barH + $gap)
    $w = $maxW * $area / $maxArea
    $brush = New-Object System.Drawing.SolidBrush($colors[$scenario])
    $g.DrawString($scenarioLabels[$scenario], $boldFont, [System.Drawing.Brushes]::Black, 66, $y)
    $g.DrawString(("air flow: {0}B m3/s; fan: {1} TWh/y" -f ($flow / 1000000000.0).ToString("N1"), $fan.ToString("N0")), $labelFont, [System.Drawing.Brushes]::DimGray, 66, $y + 23)
    $g.FillRectangle($brush, [float]$left, [float]$y, [float]$w, [float]$barH)
    $g.DrawString(($area.ToString("N0") + " km2"), $labelFont, [System.Drawing.Brushes]::White, [float]($left + 8), [float]($y + 18))
    $brush.Dispose()
}

$full = @($summary | Where-Object { $_.target_case -eq "full_100gt_all_air" })[0]
$portfolio = @($summary | Where-Object { $_.target_case -eq "portfolio_40gt_daccs" })[0]
$netl = @($sorbentRows | Where-Object { $_.scenario -eq "netl_reference_loading" })[0]
$improved = @($sorbentRows | Where-Object { $_.scenario -eq "aether_improved_sorbent" })[0]

$calloutX = 66
$calloutY = 690
$g.DrawString("Scale checks", $sectionFont, [System.Drawing.Brushes]::Black, $calloutX, $calloutY)
$calloutLines = @(
    ("100 Gt all-air, NASEM reference: {0} km2 face area; {1} one-Mt/y plant equivalents." -f ([double]$full.nasem_reference_area_km2).ToString("N0"), ([double]$full.one_mt_plant_equivalents).ToString("N0")),
    ("Current 40 Gt/y DACCS allocation: {0} km2 face area; {1} STRATOS-scale equivalents." -f ([double]$portfolio.nasem_reference_area_km2).ToString("N0"), ([double]$portfolio.stratos_500kt_equivalents).ToString("N0")),
    ("100 Gt all-air equals {0} Mammoth-scale plants or {1} STRATOS-scale plants." -f ([double]$full.mammoth_36kt_equivalents).ToString("N0"), ([double]$full.stratos_500kt_equivalents).ToString("N0")),
    ("NETL-style sorbent reference: {0} Mt inventory; {1} Mt/y replacement." -f ([double]$netl.sorbent_inventory_mt).ToString("N1"), ([double]$netl.sorbent_replacement_mt_y).ToString("N1")),
    ("AETHER improved sorbent case: {0} Mt inventory; {1} Mt/y replacement." -f ([double]$improved.sorbent_inventory_mt).ToString("N1"), ([double]$improved.sorbent_replacement_mt_y).ToString("N1"))
)
for ($k = 0; $k -lt $calloutLines.Count; $k++) {
    $g.DrawString($calloutLines[$k], $labelFont, [System.Drawing.Brushes]::DimGray, $calloutX, $calloutY + 38 + $k * 34)
}

$g.DrawString("This is plant-scale arithmetic, not a final DAC design. Flow distribution, recirculation, plume mixing, humidity, fouling, maintenance, and factory throughput still need engineering models.", $labelFont, [System.Drawing.Brushes]::DimGray, 66, 970)
$g.DrawString("Source: aether_air_contactor_scale.csv, aether_sorbent_inventory_scale.csv, and aether_air_contactor_scale_summary.csv.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 42)

Save-Png $bmp (Join-Path $FigureDir "air_contactor_physical_scale_100gt.png")
$titleFont.Dispose(); $subFont.Dispose(); $sectionFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose(); $gridPen.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "air_contactor_physical_scale_100gt.png") | Select-Object FullName,Length
