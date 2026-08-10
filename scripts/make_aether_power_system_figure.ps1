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

$rows = @(Import-Csv (Join-Path $TableDir "aether_clean_power_portfolio_requirements.csv") | Where-Object { $_.scenario -ne "advanced_3gj_full_splitting_balanced" })
$summary = @(Import-Csv (Join-Path $TableDir "aether_clean_power_portfolio_summary.csv"))
$scenarioOrder = @(
    "near_thermo_balanced_firm",
    "portfolio_lifecycle_balanced_firm",
    "advanced_3gj_balanced_firm",
    "advanced_3gj_solar_heavy"
)
$techOrder = @("utility_solar_pv", "land_based_wind", "nuclear_fission", "advanced_geothermal")
$techLabels = @{
    utility_solar_pv = "Solar PV"
    land_based_wind = "Wind"
    nuclear_fission = "Nuclear"
    advanced_geothermal = "Geothermal"
}
$scenarioLabels = @{
    near_thermo_balanced_firm = "1 GJ balanced"
    portfolio_lifecycle_balanced_firm = "Portfolio/lifecycle"
    advanced_3gj_balanced_firm = "3 GJ balanced"
    advanced_3gj_solar_heavy = "3 GJ solar-heavy"
}
$colors = @{
    utility_solar_pv = [System.Drawing.Color]::FromArgb(218, 150, 62)
    land_based_wind = [System.Drawing.Color]::FromArgb(64, 134, 160)
    nuclear_fission = [System.Drawing.Color]::FromArgb(88, 142, 84)
    advanced_geothermal = [System.Drawing.Color]::FromArgb(132, 101, 158)
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

$g.DrawString("AETHER Clean-Power Capacity Requirements", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("100 GtCO2/year is a power-system problem: even advanced capture implies tens of terawatts of new clean capacity.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 420
$top = 165
$barH = 52
$gap = 68
$maxTw = 42.0
$maxW = 980
$g.DrawString("Installed nameplate capacity by clean-power portfolio", $sectionFont, [System.Drawing.Brushes]::Black, 66, 122)
for ($tick = 0; $tick -le 40; $tick += 10) {
    $x = $left + $maxW * $tick / $maxTw
    $g.DrawLine($gridPen, [float]$x, $top - 10, [float]$x, $top + ($barH + $gap) * $scenarioOrder.Count - $gap + 28)
    $g.DrawString(($tick.ToString() + " TW"), $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 16), $top + ($barH + $gap) * $scenarioOrder.Count - 22)
}

for ($i = 0; $i -lt $scenarioOrder.Count; $i++) {
    $scenario = $scenarioOrder[$i]
    $y = $top + $i * ($barH + $gap)
    $scenarioSummary = @($summary | Where-Object { $_.scenario -eq $scenario })[0]
    $g.DrawString($scenarioLabels[$scenario], $boldFont, [System.Drawing.Brushes]::Black, 66, $y)
    $g.DrawString(("gross gen: {0} TWh/y; total: {1} TW" -f ([double]$scenarioSummary.gross_generation_with_penalty_twh_y).ToString("N0"), $scenarioSummary.total_required_nameplate_capacity_tw), $labelFont, [System.Drawing.Brushes]::DimGray, 66, $y + 22)
    $x0 = $left
    foreach ($tech in $techOrder) {
        $row = @($rows | Where-Object { $_.scenario -eq $scenario -and $_.technology -eq $tech })[0]
        $tw = [double]$row.required_nameplate_capacity_gw / 1000.0
        $w = $maxW * $tw / $maxTw
        $brush = New-Object System.Drawing.SolidBrush($colors[$tech])
        $g.FillRectangle($brush, [float]$x0, [float]$y, [float]$w, [float]$barH)
        if ($w -gt 56) {
            $g.DrawString($techLabels[$tech], $labelFont, [System.Drawing.Brushes]::White, [float]($x0 + 6), [float]($y + 16))
        }
        $x0 += $w
        $brush.Dispose()
    }
}

$legendX = 66
$legendY = 690
$g.DrawString("Technology colors", $sectionFont, [System.Drawing.Brushes]::Black, $legendX, $legendY)
for ($j = 0; $j -lt $techOrder.Count; $j++) {
    $tech = $techOrder[$j]
    $brush = New-Object System.Drawing.SolidBrush($colors[$tech])
    $g.FillRectangle($brush, $legendX, $legendY + 38 + $j * 34, 22, 18)
    $g.DrawString($techLabels[$tech], $labelFont, [System.Drawing.Brushes]::Black, $legendX + 32, $legendY + 35 + $j * 34)
    $brush.Dispose()
}

$calloutX = 545
$calloutY = 690
$g.DrawString("Scale checks", $sectionFont, [System.Drawing.Brushes]::Black, $calloutX, $calloutY)
$balanced = @($summary | Where-Object { $_.scenario -eq "advanced_3gj_balanced_firm" })[0]
$solarHeavy = @($summary | Where-Object { $_.scenario -eq "advanced_3gj_solar_heavy" })[0]
$fullSplit = @($summary | Where-Object { $_.scenario -eq "advanced_3gj_full_splitting_balanced" })[0]
$lines = @(
    ("3 GJ balanced: {0} TW nameplate; {1} TW firm clean capacity." -f $balanced.total_required_nameplate_capacity_tw, $balanced.firm_clean_capacity_tw),
    ("3 GJ solar-heavy: {0} TW nameplate; solar land proxy {1} km2." -f $solarHeavy.total_required_nameplate_capacity_tw, ([double]$solarHeavy.solar_total_area_proxy_km2).ToString("N0")),
    ("Short-duration storage proxy for 3 GJ balanced: {0} GWh at four hours." -f ([double]$balanced.four_hour_storage_proxy_energy_gwh).ToString("N0")),
    ("Full splitting warning: {0} TW nameplate, omitted from bars to preserve scale." -f $fullSplit.total_required_nameplate_capacity_tw)
)
for ($k = 0; $k -lt $lines.Count; $k++) {
    $g.DrawString($lines[$k], $labelFont, [System.Drawing.Brushes]::DimGray, $calloutX, $calloutY + 38 + $k * 34)
}

$g.DrawString("This is capacity arithmetic, not dispatch modeling. Transmission, siting, seasonal storage, curtailment, and reliability still need a power-system model.", $labelFont, [System.Drawing.Brushes]::DimGray, 66, 970)
$g.DrawString("Source: aether_clean_power_portfolio_requirements.csv and aether_clean_power_portfolio_summary.csv.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 42)

Save-Png $bmp (Join-Path $FigureDir "clean_energy_capacity_requirements_100gt.png")
$titleFont.Dispose(); $subFont.Dispose(); $sectionFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose(); $gridPen.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "clean_energy_capacity_requirements_100gt.png") | Select-Object FullName,Length
