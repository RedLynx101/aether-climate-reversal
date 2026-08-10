$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$Table = Join-Path $Root "analysis\tables\aether_climate_emulator_pathways.csv"
$Output = Join-Path $Root "analysis\figures\climate_emulator_temperature_paths.png"

if (-not (Test-Path -LiteralPath $Table)) {
    throw "Missing climate emulator pathway table: $Table"
}

$rows = @(Import-Csv -LiteralPath $Table)

$seriesSpecs = @(
    [pscustomobject]@{
        Case = "baseline_constant_emissions_no_aether"
        Policy = "nonco2_delay_aerosol_unmasking"
        Label = "No AETHER; delayed non-CO2 + aerosol unmasking"
        Color = [System.Drawing.Color]::FromArgb(172, 52, 42)
        Dash = [System.Drawing.Drawing2D.DashStyle]::Solid
        Width = 4
    },
    [pscustomobject]@{
        Case = "aether_constant_emissions_58pct_rebound"
        Policy = "nonco2_delay_aerosol_unmasking"
        Label = "AETHER with 58% rebound; same forcing stress"
        Color = [System.Drawing.Color]::FromArgb(226, 124, 44)
        Dash = [System.Drawing.Drawing2D.DashStyle]::Dash
        Width = 4
    },
    [pscustomobject]@{
        Case = "aether_net_zero_2050"
        Policy = "mitigation_with_aerosol_cleanup"
        Label = "AETHER + net-zero 2050; mitigation cleanup"
        Color = [System.Drawing.Color]::FromArgb(35, 120, 102)
        Dash = [System.Drawing.Drawing2D.DashStyle]::Solid
        Width = 4
    },
    [pscustomobject]@{
        Case = "aether_net_zero_2050"
        Policy = "active_full_forcing_management"
        Label = "AETHER + net-zero 2050; full-forcing management"
        Color = [System.Drawing.Color]::FromArgb(40, 86, 158)
        Dash = [System.Drawing.Drawing2D.DashStyle]::Solid
        Width = 4
    },
    [pscustomobject]@{
        Case = "aether_constant_emissions_no_rebound"
        Policy = "co2_only_screen"
        Label = "AETHER; CO2-only dynamic comparison"
        Color = [System.Drawing.Color]::FromArgb(91, 93, 105)
        Dash = [System.Drawing.Drawing2D.DashStyle]::Dot
        Width = 3
    }
)

$series = foreach ($spec in $seriesSpecs) {
    $points = @(
        $rows |
            Where-Object { $_.case -eq $spec.Case -and $_.forcing_policy -eq $spec.Policy } |
            Sort-Object {[int]$_.year}
    )
    if ($points.Count -eq 0) {
        throw "No climate emulator rows found for $($spec.Case) / $($spec.Policy)"
    }
    [pscustomobject]@{
        Spec = $spec
        Points = $points
    }
}

$allTemps = @($series | ForEach-Object { $_.Points } | ForEach-Object { [double]$_.surface_temperature_anomaly_c })
$minTemp = ($allTemps | Measure-Object -Minimum).Minimum
$maxTemp = ($allTemps | Measure-Object -Maximum).Maximum
$yMin = [math]::Floor(($minTemp - 0.15) * 10) / 10
$yMax = [math]::Ceiling(($maxTemp + 0.15) * 10) / 10
if ($yMax -le $yMin) {
    $yMax = $yMin + 1
}

$width = 1500
$height = 900
$left = 115
$top = 140
$plotWidth = 910
$plotHeight = 545
$right = $left + $plotWidth
$bottom = $top + $plotHeight

$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

$bg = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(250, 250, 248))
$axisBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(34, 38, 45))
$mutedBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(88, 94, 103))
$gridPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(216, 220, 224)), 1
$axisPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(38, 43, 50)), 2
$titleFont = New-Object System.Drawing.Font "Segoe UI", 28, ([System.Drawing.FontStyle]::Bold)
$subtitleFont = New-Object System.Drawing.Font "Segoe UI", 15, ([System.Drawing.FontStyle]::Regular)
$axisFont = New-Object System.Drawing.Font "Segoe UI", 13, ([System.Drawing.FontStyle]::Regular)
$labelFont = New-Object System.Drawing.Font "Segoe UI", 12, ([System.Drawing.FontStyle]::Regular)
$legendFont = New-Object System.Drawing.Font "Segoe UI", 12, ([System.Drawing.FontStyle]::Regular)
$legendTitleFont = New-Object System.Drawing.Font "Segoe UI", 13, ([System.Drawing.FontStyle]::Bold)

$g.FillRectangle($bg, 0, 0, $width, $height)
$g.DrawString("AETHER climate emulator screen", $titleFont, $axisBrush, 64, 40)
$g.DrawString("Dynamic ocean-lag response plus explicit non-CO2 and aerosol forcing scenarios; screening model, not a forecast.", $subtitleFont, $mutedBrush, 66, 82)

function Get-X([int]$Year) {
    return $left + (($Year - 2026) / (2100 - 2026)) * $plotWidth
}

function Get-Y([double]$Temp) {
    return $bottom - (($Temp - $yMin) / ($yMax - $yMin)) * $plotHeight
}

for ($year = 2030; $year -le 2100; $year += 10) {
    $x = Get-X $year
    $g.DrawLine($gridPen, [float]$x, [float]$top, [float]$x, [float]$bottom)
    $g.DrawString([string]$year, $axisFont, $mutedBrush, [float]($x - 18), [float]($bottom + 12))
}

$tick = [math]::Ceiling($yMin * 2) / 2
while ($tick -le $yMax + 0.0001) {
    $y = Get-Y $tick
    $g.DrawLine($gridPen, [float]$left, [float]$y, [float]$right, [float]$y)
    $g.DrawString($tick.ToString("0.0"), $axisFont, $mutedBrush, 48, [float]($y - 10))
    $tick += 0.5
}

$g.DrawLine($axisPen, $left, $bottom, $right, $bottom)
$g.DrawLine($axisPen, $left, $top, $left, $bottom)
$g.DrawString("Temperature anomaly, deg C", $axisFont, $axisBrush, [float]$left, 113)
$g.DrawString("Year", $axisFont, $axisBrush, [float]($left + 420), [float]($bottom + 48))

foreach ($item in $series) {
    $pen = New-Object System.Drawing.Pen $item.Spec.Color, $item.Spec.Width
    $pen.DashStyle = $item.Spec.Dash
    $previous = $null
    foreach ($point in $item.Points) {
        $x = Get-X ([int]$point.year)
        $y = Get-Y ([double]$point.surface_temperature_anomaly_c)
        if ($null -ne $previous) {
            $g.DrawLine($pen, [float]$previous.X, [float]$previous.Y, [float]$x, [float]$y)
        }
        $previous = [pscustomobject]@{ X = $x; Y = $y }
    }
    $pen.Dispose()
}

$legendX = 1070
$legendY = 150
$g.DrawString("Scenario paths", $legendTitleFont, $axisBrush, $legendX, $legendY)
$legendY += 36
foreach ($item in $series) {
    $pen = New-Object System.Drawing.Pen $item.Spec.Color, $item.Spec.Width
    $pen.DashStyle = $item.Spec.Dash
    $g.DrawLine($pen, $legendX, $legendY + 10, $legendX + 48, $legendY + 10)
    $g.DrawString($item.Spec.Label, $legendFont, $axisBrush, $legendX + 60, $legendY)
    $legendY += 54
    $pen.Dispose()
}

$note = "Interpretation: AETHER CO2 removal lowers the CO2-forcing path, but delayed non-CO2 mitigation and aerosol unmasking can hold warming high. The full-forcing management case shows why climate reversal cannot be only a CO2-machine argument."
$g.DrawString($note, $subtitleFont, $mutedBrush, (New-Object System.Drawing.RectangleF 64, 760, 1350, 58))
$g.DrawString("Source: aether_climate_emulator_model.py; two-box screening emulator calibrated to ECS=3.0 C and TCR about 1.8 C.", $labelFont, $mutedBrush, 64, 842)

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()

Write-Host "Wrote $Output"

