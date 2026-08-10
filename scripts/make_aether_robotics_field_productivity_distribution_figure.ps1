param(
    [string]$Root = "",
    [string]$Output = ""
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

if ([string]::IsNullOrWhiteSpace($Root)) {
    $Root = Split-Path -Parent $PSScriptRoot
}

if ([string]::IsNullOrWhiteSpace($Output)) {
    $Output = Join-Path $Root "analysis\figures\robotics_field_productivity_distribution_gate.png"
}

$summaryPath = Join-Path $Root "analysis\tables\aether_robotics_field_productivity_distribution_summary.csv"
$rows = @(Import-Csv -LiteralPath $summaryPath)
if ($rows.Count -lt 3) {
    throw "Expected at least three robotics field-productivity summary rows."
}

function To-Double {
    param([Parameter(Mandatory = $true)][object]$Value)
    return [double]::Parse([string]$Value, [System.Globalization.CultureInfo]::InvariantCulture)
}

function X-Log {
    param([double]$Value, [double]$Min, [double]$Max, [double]$Left, [double]$Width)
    $v = [math]::Max($Value, $Min)
    return $Left + (([math]::Log10($v) - [math]::Log10($Min)) / ([math]::Log10($Max) - [math]::Log10($Min))) * $Width
}

function Format-Robots {
    param([double]$Value)
    if ($Value -ge 1000000) {
        return ($Value / 1000000.0).ToString("0.00", [System.Globalization.CultureInfo]::InvariantCulture) + "M/y"
    }
    return $Value.ToString("N0", [System.Globalization.CultureInfo]::InvariantCulture) + "/y"
}

$width = 1600
$height = 1040
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

$white = [System.Drawing.Brushes]::White
$g.FillRectangle($white, 0, 0, $width, $height)

$titleFont = New-Object System.Drawing.Font "Segoe UI", 30, ([System.Drawing.FontStyle]::Bold)
$subtitleFont = New-Object System.Drawing.Font "Segoe UI", 15, ([System.Drawing.FontStyle]::Regular)
$labelFont = New-Object System.Drawing.Font "Segoe UI", 13, ([System.Drawing.FontStyle]::Regular)
$labelBold = New-Object System.Drawing.Font "Segoe UI", 13, ([System.Drawing.FontStyle]::Bold)
$smallFont = New-Object System.Drawing.Font "Segoe UI", 10, ([System.Drawing.FontStyle]::Regular)
$tinyFont = New-Object System.Drawing.Font "Segoe UI", 9, ([System.Drawing.FontStyle]::Regular)

$ink = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(15, 23, 42))
$muted = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(71, 85, 105))
$gridPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(220, 226, 235)), 1
$axisPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(71, 85, 105)), 2
$rangePen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(126, 87, 194)), 16
$medianPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(20, 184, 166)), 6
$ifrPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(47, 133, 90)), 3
$ifrPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash

$g.DrawString("AETHER robotics field-productivity distribution gate", $titleFont, $ink, 62, 44)
$g.DrawString("P10-P90 annual robot production after uptime, autonomy, task-fit, maintenance, and supervision multipliers. Count basis only; task suitability still has to be proven.", $subtitleFont, $muted, 64, 91)

$plotLeft = 430.0
$plotTop = 185.0
$plotWidth = 870.0
$rowGap = 135.0
$minX = 30000.0
$maxX = 30000000.0
$ticks = @(30000.0, 100000.0, 300000.0, 1000000.0, 3000000.0, 10000000.0, 30000000.0)

foreach ($tick in $ticks) {
    $x = X-Log $tick $minX $maxX $plotLeft $plotWidth
    $g.DrawLine($gridPen, [float]$x, 150, [float]$x, 650)
    $tickText = if ($tick -ge 1000000) { (($tick / 1000000).ToString("0.#", [System.Globalization.CultureInfo]::InvariantCulture) + "M") } elseif ($tick -ge 1000) { (($tick / 1000).ToString("0", [System.Globalization.CultureInfo]::InvariantCulture) + "k") } else { [string][int]$tick }
    $g.DrawString($tickText, $smallFont, $muted, [float]($x - 18), 660)
}
$g.DrawLine($axisPen, [float]$plotLeft, 650, [float]($plotLeft + $plotWidth), 650)
$g.DrawString("robots per year, log scale", $smallFont, $ink, [float]$plotLeft, 692)

$ifr = 542076.0
$ifrX = X-Log $ifr $minX $maxX $plotLeft $plotWidth
$g.DrawLine($ifrPen, [float]$ifrX, 150, [float]$ifrX, 650)
$g.DrawString("IFR 2024 installs", $smallFont, (New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(47, 133, 90))), [float]($ifrX + 8), 154)

$order = @(
    "high_robot_intensity_translation",
    "aether_automation_push",
    "deep_modular_abundance"
)

$nameMap = @{
    high_robot_intensity_translation = "High robot intensity"
    aether_automation_push = "AETHER automation push"
    deep_modular_abundance = "Deep modular abundance"
}

for ($i = 0; $i -lt $order.Count; $i++) {
    $scenario = $order[$i]
    $row = $rows | Where-Object { $_.scenario -eq $scenario } | Select-Object -First 1
    if (-not $row) {
        throw "Missing summary row for $scenario"
    }
    $y = $plotTop + ($i * $rowGap)
    $p10 = To-Double $row.annual_production_p10_robots
    $p50 = To-Double $row.annual_production_p50_robots
    $p90 = To-Double $row.annual_production_p90_robots
    $pass = (To-Double $row.ifr_pass_share) * 100.0
    $eff = To-Double $row.effective_multiplier_p50
    $stock = To-Double $row.robot_stock_p50_million

    $x10 = X-Log $p10 $minX $maxX $plotLeft $plotWidth
    $x50 = X-Log $p50 $minX $maxX $plotLeft $plotWidth
    $x90 = X-Log $p90 $minX $maxX $plotLeft $plotWidth

    $g.DrawString($nameMap[$scenario], $labelBold, $ink, 64, [float]($y - 18))
    $g.DrawString(("P50 stock " + $stock.ToString("0.00", [System.Globalization.CultureInfo]::InvariantCulture) + "M; P50 field multiplier " + $eff.ToString("0.00", [System.Globalization.CultureInfo]::InvariantCulture)), $smallFont, $muted, 64, [float]($y + 8))
    $g.DrawLine($rangePen, [float]$x10, [float]$y, [float]$x90, [float]$y)
    $g.DrawLine($medianPen, [float]$x50, [float]($y - 28), [float]$x50, [float]($y + 28))
    $g.DrawString((Format-Robots $p50), $labelBold, $ink, [float]($x50 + 10), [float]($y - 32))
    $g.DrawString(("IFR pass share " + $pass.ToString("0", [System.Globalization.CultureInfo]::InvariantCulture) + "%"), $smallFont, $muted, [float]($x50 + 10), [float]($y - 8))
}

$legendY = 740
$g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(126, 87, 194))), 64, $legendY, 28, 16)
$g.DrawString("P10-P90 range", $smallFont, $ink, 102, [float]($legendY - 3))
$g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(20, 184, 166))), 235, $legendY, 10, 28)
$g.DrawString("P50", $smallFont, $ink, 257, [float]($legendY - 3))
$g.DrawLine($ifrPen, 330, [float]($legendY + 8), 390, [float]($legendY + 8))
$g.DrawString("current annual industrial robot installs", $smallFont, $ink, 404, [float]($legendY - 3))

$note = "Interpretation: production-rate optimism is fragile if field productivity is weak. The automation-push case can look plausible on simple count, but after uptime, autonomy, task-fit, maintenance, and supervision penalties it often moves back toward today's entire industrial-robot installation scale. That is a testable requirement, not a slogan."
$g.DrawString($note, $subtitleFont, $muted, (New-Object System.Drawing.RectangleF 64, 800, 1430, 108))
$g.DrawString("Source: aether_robotics_field_productivity_distribution_model.py, using aether_robotics_productivity_by_task.csv. Multipliers are scenario distributions that require source-backed task tests before publication-grade claims.", $smallFont, $muted, (New-Object System.Drawing.RectangleF 64, 930, 1430, 55))

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()

Write-Host "Wrote $Output"

