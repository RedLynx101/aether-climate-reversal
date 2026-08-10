param(
    [string]$SummaryPath = (Join-Path $PSScriptRoot "..\analysis\tables\aether_state_dependent_carbon_summary.csv"),
    [string]$Output = (Join-Path $PSScriptRoot "..\analysis\figures\state_dependent_carbon_removal_effectiveness.png")
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$rows = Import-Csv -LiteralPath $SummaryPath
$selectedCases = @(
    "aether_net_zero_2050",
    "aether_constant_emissions_no_rebound",
    "aether_constant_emissions_58pct_rebound"
)
$caseLabels = @{
    "aether_net_zero_2050" = "Net-zero 2050"
    "aether_constant_emissions_no_rebound" = "Constant emissions"
    "aether_constant_emissions_58pct_rebound" = "58% rebound"
}
$effectivenessCases = @(
    "fixed_0p96_current",
    "optimistic_active_management",
    "conservative_state_dependent",
    "asymmetry_stress"
)
$effectivenessLabels = @{
    "fixed_0p96_current" = "Fixed 0.96"
    "optimistic_active_management" = "Optimistic"
    "conservative_state_dependent" = "Conservative"
    "asymmetry_stress" = "Asymmetry stress"
}
$colors = @{
    "fixed_0p96_current" = [System.Drawing.Color]::FromArgb(86, 86, 94)
    "optimistic_active_management" = [System.Drawing.Color]::FromArgb(39, 137, 112)
    "conservative_state_dependent" = [System.Drawing.Color]::FromArgb(48, 102, 190)
    "asymmetry_stress" = [System.Drawing.Color]::FromArgb(192, 89, 77)
}

$width = 1500
$height = 920
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::FromArgb(249, 249, 247))

$titleFont = New-Object System.Drawing.Font("Segoe UI Semibold", 30)
$subtitleFont = New-Object System.Drawing.Font("Segoe UI", 15)
$axisFont = New-Object System.Drawing.Font("Segoe UI", 13)
$smallFont = New-Object System.Drawing.Font("Segoe UI", 11)
$titleBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(30, 36, 43))
$mutedBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(87, 94, 103))
$axisBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(50, 56, 64))
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(222, 226, 230), 1)
$floorPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(30, 36, 43), 2)
$floorPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash

$g.DrawString("AETHER State-Dependent Removal Effectiveness", $titleFont, $titleBrush, 56, 36)
$g.DrawString("2100 atmospheric CO2 in a reduced-form screen; lower multipliers represent land/ocean compensation and reversal asymmetry.", $subtitleFont, $mutedBrush, 58, 88)

$plotX = 250
$plotY = 160
$plotW = 1120
$plotH = 540
$xMin = 340.0
$xMax = 520.0

function Map-X([double]$value) {
    return $plotX + (($value - $xMin) / ($xMax - $xMin)) * $plotW
}

foreach ($tick in 350, 400, 450, 500) {
    $x = Map-X $tick
    $g.DrawLine($gridPen, [float]$x, [float]$plotY, [float]$x, [float]($plotY + $plotH))
    $g.DrawString("$tick ppm", $smallFont, $mutedBrush, [float]($x - 22), [float]($plotY + $plotH + 12))
}
$floorX = Map-X 350
$g.DrawLine($floorPen, [float]$floorX, [float]($plotY - 8), [float]$floorX, [float]($plotY + $plotH))
$g.DrawString("350 ppm management floor", $smallFont, $axisBrush, [float]($floorX + 8), [float]($plotY - 26))

$groupH = 150
$barH = 22
$gap = 7
for ($i = 0; $i -lt $selectedCases.Count; $i++) {
    $case = $selectedCases[$i]
    $baseY = $plotY + 36 + $i * $groupH
    $g.DrawString($caseLabels[$case], $axisFont, $axisBrush, 56, [float]($baseY + 32))
    for ($j = 0; $j -lt $effectivenessCases.Count; $j++) {
        $eff = $effectivenessCases[$j]
        $row = $rows | Where-Object { $_.base_case -eq $case -and $_.effectiveness_case -eq $eff } | Select-Object -First 1
        if (-not $row) {
            throw "Missing summary row for $case / $eff"
        }
        $ppm = [double]$row.co2_ppm_2100
        $y = $baseY + $j * ($barH + $gap)
        $x0 = Map-X $xMin
        $x1 = Map-X $ppm
        $brush = New-Object System.Drawing.SolidBrush($colors[$eff])
        $g.FillRectangle($brush, [float]$x0, [float]$y, [float]($x1 - $x0), [float]$barH)
        $brush.Dispose()
        $g.DrawString($ppm.ToString("0.0") + " ppm", $smallFont, $axisBrush, [float]($x1 + 8), [float]($y - 1))
    }
}

$legendX = 250
$legendY = 735
for ($j = 0; $j -lt $effectivenessCases.Count; $j++) {
    $eff = $effectivenessCases[$j]
    $x = $legendX + $j * 260
    $brush = New-Object System.Drawing.SolidBrush($colors[$eff])
    $g.FillRectangle($brush, $x, $legendY, 24, 16)
    $brush.Dispose()
    $g.DrawString($effectivenessLabels[$eff], $axisFont, $axisBrush, $x + 34, $legendY - 3)
}

$note = "Read: fixed removal effectiveness can make AETHER look cleaner than the climate-carbon system warrants. This screen penalizes effectiveness as drawdown deepens and removals outrun positive emissions. It is still not FAIR or an Earth-system model."
$g.DrawString($note, $subtitleFont, $mutedBrush, (New-Object System.Drawing.RectangleF 58, 790, 1360, 54))
$g.DrawString("Source: aether_state_dependent_carbon_model.py. The multipliers are scenario screens calibrated from carbon-cycle literature warnings, not fitted climate-model outputs.", $smallFont, $mutedBrush, 58, 866)

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()

Write-Host "Wrote $Output"

