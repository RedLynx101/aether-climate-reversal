$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$PathwayPath = Join-Path $Root "analysis\tables\aether_fair_forcing_temperature_paths.csv"
$DeltaPath = Join-Path $Root "analysis\tables\aether_fair_forcing_delta_vs_emulator.csv"
$Output = Join-Path $Root "analysis\figures\fair_forcing_execution_comparison.png"

$rows = @(Import-Csv -LiteralPath $PathwayPath)
$deltaRows = @(Import-Csv -LiteralPath $DeltaPath)

function To-Double {
    param([Parameter(Mandatory = $true)]$Value)
    return [double]::Parse([string]$Value, [System.Globalization.CultureInfo]::InvariantCulture)
}

function Get-X {
    param([int]$Year)
    return $left + (($Year - 2026) / (2100 - 2026)) * $plotWidth
}

function Get-Y {
    param([double]$Temperature)
    return $bottom - (($Temperature - $yMin) / ($yMax - $yMin)) * $plotHeight
}

function Draw-Series {
    param(
        [array]$SeriesRows,
        [System.Drawing.Pen]$Pen
    )
    $ordered = @($SeriesRows | Sort-Object {[int]$_.year})
    for ($i = 1; $i -lt $ordered.Count; $i++) {
        $a = $ordered[$i - 1]
        $b = $ordered[$i]
        $g.DrawLine(
            $Pen,
            [float](Get-X ([int]$a.year)),
            [float](Get-Y (To-Double $a.fair_surface_temperature_c)),
            [float](Get-X ([int]$b.year)),
            [float](Get-Y (To-Double $b.fair_surface_temperature_c))
        )
    }
}

$width = 1600
$height = 980
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font "Segoe UI", 28, ([System.Drawing.FontStyle]::Bold)
$subtitleFont = New-Object System.Drawing.Font "Segoe UI", 14, ([System.Drawing.FontStyle]::Regular)
$labelFont = New-Object System.Drawing.Font "Segoe UI", 12, ([System.Drawing.FontStyle]::Regular)
$labelBold = New-Object System.Drawing.Font "Segoe UI", 12, ([System.Drawing.FontStyle]::Bold)
$smallFont = New-Object System.Drawing.Font "Segoe UI", 10, ([System.Drawing.FontStyle]::Regular)

$ink = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(15, 23, 42))
$muted = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(71, 85, 105))
$gridPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(226, 232, 240)), 1
$axisPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(71, 85, 105)), 2
$baselinePen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(190, 64, 64)), 4
$reboundPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(126, 87, 194)), 4
$netZeroPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(20, 148, 136)), 4
$noReboundPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(37, 99, 235)), 3

$g.DrawString("AETHER forcing-driven FAIR execution", $titleFont, $ink, 64, 42)
$g.DrawString("FAIR 2.2.4 package run using AETHER CO2, aggregate non-CO2, and aerosol forcing paths. Diagnostic, not a full species-emissions run.", $subtitleFont, $muted, 66, 91)

$left = 92.0
$top = 170.0
$plotWidth = 820.0
$plotHeight = 520.0
$bottom = $top + $plotHeight
$yMin = 0.75
$yMax = 4.25

foreach ($temp in @(1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0)) {
    $y = Get-Y $temp
    $g.DrawLine($gridPen, [float]$left, [float]$y, [float]($left + $plotWidth), [float]$y)
    $g.DrawString($temp.ToString("0.0", [System.Globalization.CultureInfo]::InvariantCulture) + " C", $smallFont, $muted, 34, [float]($y - 8))
}
foreach ($year in @(2026, 2040, 2060, 2080, 2100)) {
    $x = Get-X $year
    $g.DrawLine($gridPen, [float]$x, [float]$top, [float]$x, [float]$bottom)
    $g.DrawString([string]$year, $smallFont, $muted, [float]($x - 18), [float]($bottom + 16))
}
$g.DrawLine($axisPen, [float]$left, [float]$bottom, [float]($left + $plotWidth), [float]$bottom)
$g.DrawLine($axisPen, [float]$left, [float]$top, [float]$left, [float]$bottom)
$g.DrawString("FAIR surface temperature anomaly, C", $smallFont, $ink, [float]$left, [float]($top - 28))

$baselineRows = @($rows | Where-Object { $_.case -eq "baseline_constant_emissions_no_aether" -and $_.forcing_policy -eq "nonco2_delay_aerosol_unmasking" -and $_.config -eq "central_diagnostic" })
$reboundRows = @($rows | Where-Object { $_.case -eq "aether_constant_emissions_58pct_rebound" -and $_.forcing_policy -eq "nonco2_delay_aerosol_unmasking" -and $_.config -eq "central_diagnostic" })
$netZeroRows = @($rows | Where-Object { $_.case -eq "aether_net_zero_2050" -and $_.forcing_policy -eq "active_full_forcing_management" -and $_.config -eq "central_diagnostic" })
$noReboundRows = @($rows | Where-Object { $_.case -eq "aether_constant_emissions_no_rebound" -and $_.forcing_policy -eq "active_full_forcing_management" -and $_.config -eq "central_diagnostic" })

Draw-Series $baselineRows $baselinePen
Draw-Series $reboundRows $reboundPen
Draw-Series $netZeroRows $netZeroPen
Draw-Series $noReboundRows $noReboundPen

$legendX = 100
$legendY = 730
$legendItems = @(
    @("No AETHER, delayed non-CO2/aerosol stress", $baselinePen),
    @("AETHER 58% rebound, same stress", $reboundPen),
    @("AETHER net-zero 2050 plus full-forcing management", $netZeroPen),
    @("AETHER no rebound plus full-forcing management", $noReboundPen)
)
for ($i = 0; $i -lt $legendItems.Count; $i++) {
    $y = $legendY + ($i * 28)
    $g.DrawLine($legendItems[$i][1], $legendX, $y + 8, $legendX + 48, $y + 8)
    $g.DrawString($legendItems[$i][0], $smallFont, $ink, $legendX + 62, $y)
}

$panelX = 1010
$panelY = 170
$g.DrawString("FAIR minus emulator at 2100", $labelBold, $ink, $panelX, $panelY)
$g.DrawString("Central diagnostic config; positive means FAIR warmer.", $smallFont, $muted, $panelX, $panelY + 28)

$selectedDeltas = @(
    @("No AETHER stress", "baseline_constant_emissions_no_aether", "nonco2_delay_aerosol_unmasking"),
    @("AETHER 58% rebound", "aether_constant_emissions_58pct_rebound", "nonco2_delay_aerosol_unmasking"),
    @("AETHER net-zero", "aether_net_zero_2050", "active_full_forcing_management"),
    @("AETHER no rebound", "aether_constant_emissions_no_rebound", "active_full_forcing_management")
)
$zeroX = $panelX + 210
$scale = 170.0
$deltaPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(71, 85, 105)), 2
$g.DrawLine($deltaPen, $zeroX, $panelY + 95, $zeroX, $panelY + 380)
for ($i = 0; $i -lt $selectedDeltas.Count; $i++) {
    $label = $selectedDeltas[$i][0]
    $case = $selectedDeltas[$i][1]
    $policy = $selectedDeltas[$i][2]
    $row = $deltaRows | Where-Object { $_.case -eq $case -and $_.forcing_policy -eq $policy -and $_.config -eq "central_diagnostic" } | Select-Object -First 1
    $delta = To-Double $row.fair_minus_emulator_2100_c
    $y = $panelY + 105 + ($i * 68)
    $barW = [math]::Abs($delta) * $scale
    $barX = if ($delta -ge 0) { $zeroX } else { $zeroX - $barW }
    $brushColor = if ($delta -ge 0) { [System.Drawing.Color]::FromArgb(190,64,64) } else { [System.Drawing.Color]::FromArgb(20,148,136) }
    $brush = New-Object System.Drawing.SolidBrush $brushColor
    $g.DrawString($label, $smallFont, $ink, $panelX, $y - 24)
    $g.FillRectangle($brush, [float]$barX, [float]$y, [float]$barW, 24)
    $g.DrawString($delta.ToString("+0.00;-0.00;0.00", [System.Globalization.CultureInfo]::InvariantCulture) + " C", $labelBold, $ink, [float]($zeroX + 180), [float]($y + 1))
}

$note = "Interpretation: this is now a real FAIR package execution, but only in forcing mode. It tests whether AETHER's aggregate forcing pathways produce similar temperature direction under FAIR's response engine; it does not solve missing CH4, N2O, aerosol-precursor, land-use, lifecycle, or uncertainty inputs."
$g.DrawString($note, $subtitleFont, $muted, (New-Object System.Drawing.RectangleF 64, 855, 1440, 58))
$g.DrawString("Source: aether_fair_forcing_execution_model.py using FAIR 2.2.4 and aether_fair_readiness_input_deck.csv.", $smallFont, $muted, 64, 930)

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()
Write-Host "Wrote $Output"

