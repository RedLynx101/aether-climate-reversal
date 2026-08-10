$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$DeckPath = Join-Path $Root "analysis\tables\aether_fair_readiness_input_deck.csv"
$GapPath = Join-Path $Root "analysis\tables\aether_fair_readiness_gap_matrix.csv"
$Output = Join-Path $Root "analysis\figures\fair_readiness_climate_input_deck.png"

$deck = @(Import-Csv -LiteralPath $DeckPath)
$gaps = @(Import-Csv -LiteralPath $GapPath)

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
        [array]$Rows,
        [System.Drawing.Pen]$Pen
    )
    $ordered = @($Rows | Sort-Object {[int]$_.year})
    for ($i = 1; $i -lt $ordered.Count; $i++) {
        $a = $ordered[$i - 1]
        $b = $ordered[$i]
        $g.DrawLine(
            $Pen,
            [float](Get-X ([int]$a.year)),
            [float](Get-Y (To-Double $a.surface_temperature_anomaly_c)),
            [float](Get-X ([int]$b.year)),
            [float](Get-Y (To-Double $b.surface_temperature_anomaly_c))
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

$titleFont = New-Object System.Drawing.Font "Segoe UI", 29, ([System.Drawing.FontStyle]::Bold)
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

$g.DrawString("AETHER FAIR-readiness climate input deck", $titleFont, $ink, 64, 42)
$g.DrawString("Joined annual CO2/removal pulse variables, forcing paths, and temperature-screen outputs. This is a handoff scaffold, not a FAIR result.", $subtitleFont, $muted, 66, 91)

$left = 92.0
$top = 170.0
$plotWidth = 820.0
$plotHeight = 520.0
$bottom = $top + $plotHeight
$yMin = 0.75
$yMax = 3.45

foreach ($temp in @(1.0, 1.5, 2.0, 2.5, 3.0)) {
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
$g.DrawString("temperature anomaly, C", $smallFont, $ink, [float]$left, [float]($top - 28))

$baselineRows = @($deck | Where-Object { $_.case -eq "baseline_constant_emissions_no_aether" -and $_.forcing_policy -eq "nonco2_delay_aerosol_unmasking" })
$reboundRows = @($deck | Where-Object { $_.case -eq "aether_constant_emissions_58pct_rebound" -and $_.forcing_policy -eq "nonco2_delay_aerosol_unmasking" })
$netZeroRows = @($deck | Where-Object { $_.case -eq "aether_net_zero_2050" -and $_.forcing_policy -eq "active_full_forcing_management" })
$noReboundRows = @($deck | Where-Object { $_.case -eq "aether_constant_emissions_no_rebound" -and $_.forcing_policy -eq "active_full_forcing_management" })

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
$g.DrawString("Variable-family readiness", $labelBold, $ink, $panelX, $panelY)
$g.DrawString("Status of inputs needed before a real FAIR or Earth-system run.", $smallFont, $muted, $panelX, $panelY + 28)

$statusOrder = @("usable_screen", "provisional_proxy", "aggregate_placeholder", "missing")
$statusLabels = @{
    usable_screen = "usable screen"
    provisional_proxy = "provisional proxy"
    aggregate_placeholder = "aggregate placeholder"
    missing = "missing"
}
$statusColors = @{
    usable_screen = [System.Drawing.Color]::FromArgb(20, 148, 136)
    provisional_proxy = [System.Drawing.Color]::FromArgb(37, 99, 235)
    aggregate_placeholder = [System.Drawing.Color]::FromArgb(245, 158, 11)
    missing = [System.Drawing.Color]::FromArgb(190, 64, 64)
}
$maxCount = 1
foreach ($status in $statusOrder) {
    $count = @($gaps | Where-Object { $_.current_status -eq $status }).Count
    if ($count -gt $maxCount) { $maxCount = $count }
}
for ($i = 0; $i -lt $statusOrder.Count; $i++) {
    $status = $statusOrder[$i]
    $count = @($gaps | Where-Object { $_.current_status -eq $status }).Count
    $y = $panelY + 88 + ($i * 72)
    $barWidth = 390.0 * ($count / [double]$maxCount)
    $brush = New-Object System.Drawing.SolidBrush $statusColors[$status]
    $g.FillRectangle($brush, $panelX, $y, [float]$barWidth, 26)
    $g.DrawString($statusLabels[$status], $labelFont, $ink, $panelX, $y - 24)
    $g.DrawString([string]$count, $labelBold, $ink, [float]($panelX + $barWidth + 12), [float]($y + 2))
}

$p0Gaps = @($gaps | Where-Object { $_.priority -eq "P0" -and $_.current_status -ne "usable_screen" }).Count
$totalFamilies = $gaps.Count
$g.DrawString("P0 gaps remaining: $p0Gaps of $totalFamilies variable families", $labelBold, $ink, $panelX, 535)
$g.DrawString("The deck is useful because it defines the handoff. It does not close the handoff.", $subtitleFont, $muted, (New-Object System.Drawing.RectangleF $panelX, 570, 455, 72))

$note = "Interpretation: the climate story improves when CO2, non-CO2 forcing, aerosols, ocean lag, and removals are put in one annual deck. The same table also shows why publication-grade temperature claims still require species-level trajectories, ZEC, lifecycle emissions, and uncertainty ensembles."
$g.DrawString($note, $subtitleFont, $muted, (New-Object System.Drawing.RectangleF 64, 855, 1440, 58))
$g.DrawString("Source: aether_fair_readiness_model.py joining aether_state_dependent_carbon_pathways.csv with aether_climate_emulator_pathways.csv.", $smallFont, $muted, 64, 930)

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()
Write-Host "Wrote $Output"

