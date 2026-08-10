$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$ClaimsPath = Join-Path $Root "analysis\tables\aether_robotics_production_claims.csv"
$SummaryPath = Join-Path $Root "analysis\tables\aether_robotics_production_verification_summary.csv"
$Output = Join-Path $Root "analysis\figures\robotics_production_verification_gate.png"

if (-not (Test-Path -LiteralPath $ClaimsPath)) {
    throw "Missing robotics production claims table: $ClaimsPath"
}
if (-not (Test-Path -LiteralPath $SummaryPath)) {
    throw "Missing robotics production verification summary table: $SummaryPath"
}

$claims = @(Import-Csv -LiteralPath $ClaimsPath)
$summary = @{}
Import-Csv -LiteralPath $SummaryPath | ForEach-Object {
    $summary[$_.metric] = [double]$_.value
}

function LogX {
    param(
        [Parameter(Mandatory = $true)][double]$Value,
        [Parameter(Mandatory = $true)][double]$Min,
        [Parameter(Mandatory = $true)][double]$Max,
        [Parameter(Mandatory = $true)][double]$Left,
        [Parameter(Mandatory = $true)][double]$Width
    )
    $safeValue = [Math]::Max($Value, $Min)
    return $Left + (([Math]::Log10($safeValue) - [Math]::Log10($Min)) / ([Math]::Log10($Max) - [Math]::Log10($Min))) * $Width
}

function Draw-WrappedText {
    param(
        [Parameter(Mandatory = $true)]$Graphics,
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)]$Font,
        [Parameter(Mandatory = $true)]$Brush,
        [Parameter(Mandatory = $true)][float]$X,
        [Parameter(Mandatory = $true)][float]$Y,
        [Parameter(Mandatory = $true)][float]$Width,
        [Parameter(Mandatory = $true)][float]$Height
    )
    $rect = New-Object System.Drawing.RectangleF $X, $Y, $Width, $Height
    $Graphics.DrawString($Text, $Font, $Brush, $rect)
}

$bars = @(
    [pscustomobject]@{ label = "Figure 250/month lead"; value = 3000.0; type = "social"; note = "unresolved lead" },
    [pscustomobject]@{ label = "Figure 1/hour cadence"; value = 8760.0; type = "company"; note = "company primary" },
    [pscustomobject]@{ label = "Agility RoboFab"; value = 10000.0; type = "company"; note = "company capacity" },
    [pscustomobject]@{ label = "Figure BotQ line"; value = 12000.0; type = "company"; note = "company capacity" },
    [pscustomobject]@{ label = "Deep modular AETHER"; value = $summary["deep_required_robots_y"]; type = "aether"; note = "scenario requirement" },
    [pscustomobject]@{ label = "AETHER automation push"; value = $summary["push_required_robots_y"]; type = "aether"; note = "scenario requirement" },
    [pscustomobject]@{ label = "IFR annual installs"; value = 542076.0; type = "independent"; note = "industry statistic" },
    [pscustomobject]@{ label = "High robot-intensity"; value = $summary["high_required_robots_y"]; type = "aether"; note = "scenario requirement" }
)

$colors = @{
    social = [System.Drawing.Color]::FromArgb(170, 108, 48)
    company = [System.Drawing.Color]::FromArgb(71, 116, 173)
    independent = [System.Drawing.Color]::FromArgb(55, 130, 95)
    aether = [System.Drawing.Color]::FromArgb(130, 70, 150)
}

$width = 1600
$height = 960
$left = 315
$top = 150
$plotWidth = 970
$barHeight = 42
$barGap = 26
$minX = 1000.0
$maxX = 3000000.0

$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

$bg = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(250, 250, 247))
$axisBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(32, 35, 40))
$mutedBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(89, 95, 103))
$panelBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(239, 241, 238))
$gridPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(216, 221, 223)), 1
$axisPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(70, 76, 84)), 2
$titleFont = New-Object System.Drawing.Font "Segoe UI", 27, ([System.Drawing.FontStyle]::Bold)
$subtitleFont = New-Object System.Drawing.Font "Segoe UI", 15, ([System.Drawing.FontStyle]::Regular)
$labelFont = New-Object System.Drawing.Font "Segoe UI", 12, ([System.Drawing.FontStyle]::Regular)
$smallFont = New-Object System.Drawing.Font "Segoe UI", 10, ([System.Drawing.FontStyle]::Regular)
$valueFont = New-Object System.Drawing.Font "Segoe UI", 12, ([System.Drawing.FontStyle]::Bold)
$panelTitleFont = New-Object System.Drawing.Font "Segoe UI", 15, ([System.Drawing.FontStyle]::Bold)

$g.FillRectangle($bg, 0, 0, $width, $height)
$g.DrawString("AETHER robotics production verification gate", $titleFont, $axisBrush, 58, 38)
$subtitle = "Annual robot-flow anchors versus AETHER scenario production requirements. Company claims are useful signals; social-media leads stay out of paper facts."
$g.DrawString($subtitle, $subtitleFont, $mutedBrush, 60, 82)

foreach ($tick in @(1000, 3000, 10000, 30000, 100000, 300000, 1000000, 3000000)) {
    $x = LogX -Value $tick -Min $minX -Max $maxX -Left $left -Width $plotWidth
    $g.DrawLine($gridPen, [float]$x, [float]($top - 22), [float]$x, [float]($top + $bars.Count * ($barHeight + $barGap) - 10))
    $tickLabel = if ($tick -ge 1000000) { ($tick / 1000000).ToString("0.#") + "M" } elseif ($tick -ge 1000) { ($tick / 1000).ToString("0.#") + "k" } else { [string]$tick }
    $g.DrawString($tickLabel, $smallFont, $mutedBrush, [float]($x - 18), [float]($top + $bars.Count * ($barHeight + $barGap) + 4))
}
$g.DrawLine($axisPen, [float]$left, [float]($top + $bars.Count * ($barHeight + $barGap) - 10), [float]($left + $plotWidth), [float]($top + $bars.Count * ($barHeight + $barGap) - 10))
$g.DrawString("robots per year, log scale", $smallFont, $axisBrush, $left, [float]($top + $bars.Count * ($barHeight + $barGap) + 32))

for ($i = 0; $i -lt $bars.Count; $i++) {
    $bar = $bars[$i]
    $y = $top + $i * ($barHeight + $barGap)
    $x0 = LogX -Value $minX -Min $minX -Max $maxX -Left $left -Width $plotWidth
    $x1 = LogX -Value $bar.value -Min $minX -Max $maxX -Left $left -Width $plotWidth
    $g.DrawString($bar.label, $labelFont, $axisBrush, 60, [float]($y + 9))
    $g.DrawString($bar.note, $smallFont, $mutedBrush, 60, [float]($y + 30))
    $brush = New-Object System.Drawing.SolidBrush $colors[$bar.type]
    $g.FillRectangle($brush, [float]$x0, [float]$y, [float]([Math]::Max(3, $x1 - $x0)), [float]$barHeight)
    $brush.Dispose()
    $valueLabel = $bar.value.ToString("N0", [System.Globalization.CultureInfo]::InvariantCulture) + "/y"
    $g.DrawString($valueLabel, $valueFont, $axisBrush, [float]($x1 + 10), [float]($y + 10))
}

$panelX = 1310
$panelY = 165
$panelW = 230
$panelH = 510
$g.FillRectangle($panelBrush, $panelX, $panelY, $panelW, $panelH)
$g.DrawString("BotQ-equivalent lines", $panelTitleFont, $axisBrush, $panelX + 16, $panelY + 18)
$g.DrawString("How many 12k/y lines would match each AETHER annual robot-flow case.", $smallFont, $mutedBrush, (New-Object System.Drawing.RectangleF ($panelX + 16), ($panelY + 52), ($panelW - 32), 70))

$lineRows = @(
    [pscustomobject]@{ label = "High intensity"; value = $summary["high_figure_botq_factories"] },
    [pscustomobject]@{ label = "Automation push"; value = $summary["push_figure_botq_factories"] },
    [pscustomobject]@{ label = "Deep modular"; value = $summary["deep_figure_botq_factories"] }
)
$lineTop = $panelY + 135
$maxLines = ($lineRows | ForEach-Object { $_.value } | Measure-Object -Maximum).Maximum
foreach ($row in $lineRows) {
    $barW = [Math]::Max(5, ($row.value / $maxLines) * 170)
    $g.DrawString($row.label, $labelFont, $axisBrush, $panelX + 16, [float]$lineTop)
    $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(130, 70, 150))
    $g.FillRectangle($brush, $panelX + 18, $lineTop + 28, [float]$barW, 18)
    $brush.Dispose()
    $g.DrawString($row.value.ToString("N1", [System.Globalization.CultureInfo]::InvariantCulture) + "x", $valueFont, $axisBrush, $panelX + 22 + [float]$barW, [float]($lineTop + 23))
    $lineTop += 92
}

$legendY = 760
$legendItems = @(
    [pscustomobject]@{ label = "Independent industry statistic"; type = "independent" },
    [pscustomobject]@{ label = "Company primary claim"; type = "company" },
    [pscustomobject]@{ label = "Unresolved social-media lead"; type = "social" },
    [pscustomobject]@{ label = "AETHER scenario requirement"; type = "aether" }
)
for ($i = 0; $i -lt $legendItems.Count; $i++) {
    $item = $legendItems[$i]
    $x = 60 + $i * 360
    $brush = New-Object System.Drawing.SolidBrush $colors[$item.type]
    $g.FillRectangle($brush, $x, $legendY + 4, 26, 16)
    $brush.Dispose()
    $g.DrawString($item.label, $smallFont, $axisBrush, $x + 36, $legendY)
}

$note = "Interpretation: a single frontier humanoid factory is not enough for the high-intensity AETHER case. The automation-push case is below current annual industrial robot installations on count, but still needs task suitability, uptime, service, and field-productivity evidence. The 250/month X item is kept as a lead, not a citation-grade fact."
Draw-WrappedText -Graphics $g -Text $note -Font $subtitleFont -Brush $mutedBrush -X 60 -Y 835 -Width 1450 -Height 78
$g.DrawString("Source: aether_robotics_production_verification_model.py using source-register robotics anchors and the robotics productivity summary.", $smallFont, $mutedBrush, 60, 920)

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()

Write-Host "Wrote $Output"

