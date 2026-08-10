$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$TaskPath = Join-Path $Root "analysis\tables\aether_robotics_productivity_by_task.csv"
$SummaryPath = Join-Path $Root "analysis\tables\aether_robotics_productivity_summary.csv"
$Output = Join-Path $Root "analysis\figures\robotics_productivity_capacity_stack.png"

if (-not (Test-Path -LiteralPath $TaskPath)) {
    throw "Missing robotics productivity task table: $TaskPath"
}
if (-not (Test-Path -LiteralPath $SummaryPath)) {
    throw "Missing robotics productivity summary table: $SummaryPath"
}

$taskRows = @(Import-Csv -LiteralPath $TaskPath)
$summaryRows = @(Import-Csv -LiteralPath $SummaryPath)
$scenarioOrder = @(
    "high_robot_intensity_translation",
    "aether_automation_push",
    "deep_modular_abundance"
)
$scenarioLabels = @{
    high_robot_intensity_translation = "High robot intensity"
    aether_automation_push = "AETHER automation push"
    deep_modular_abundance = "Deep modular abundance"
}
$taskOrder = @(
    "plant_operations_maintenance",
    "materials_handling_logistics",
    "storage_field_operations",
    "mrv_sensor_auditing",
    "factory_spares_replacement",
    "robotic_labs_process_improvement",
    "module_manufacturing",
    "construction_commissioning",
    "storage_wells_corridors",
    "logistics_ramp",
    "mrv_initialization"
)
$taskLabels = @{
    plant_operations_maintenance = "Plant O&M"
    materials_handling_logistics = "Logistics"
    storage_field_operations = "Storage field"
    mrv_sensor_auditing = "MRV auditing"
    factory_spares_replacement = "Spares"
    robotic_labs_process_improvement = "Robotic labs"
    module_manufacturing = "Modules"
    construction_commissioning = "Construction"
    storage_wells_corridors = "Wells/corridors"
    logistics_ramp = "Ramp logistics"
    mrv_initialization = "MRV setup"
}
$colors = @{
    plant_operations_maintenance = [System.Drawing.Color]::FromArgb(40, 94, 143)
    materials_handling_logistics = [System.Drawing.Color]::FromArgb(79, 150, 143)
    storage_field_operations = [System.Drawing.Color]::FromArgb(175, 96, 47)
    mrv_sensor_auditing = [System.Drawing.Color]::FromArgb(120, 111, 166)
    factory_spares_replacement = [System.Drawing.Color]::FromArgb(83, 133, 64)
    robotic_labs_process_improvement = [System.Drawing.Color]::FromArgb(158, 83, 127)
    module_manufacturing = [System.Drawing.Color]::FromArgb(67, 116, 191)
    construction_commissioning = [System.Drawing.Color]::FromArgb(190, 123, 43)
    storage_wells_corridors = [System.Drawing.Color]::FromArgb(130, 85, 57)
    logistics_ramp = [System.Drawing.Color]::FromArgb(68, 154, 111)
    mrv_initialization = [System.Drawing.Color]::FromArgb(120, 142, 196)
}

$maxHours = 0.0
foreach ($scenario in $scenarioOrder) {
    $total = ($taskRows | Where-Object { $_.scenario -eq $scenario } | ForEach-Object { [double]$_.annual_useful_task_hours_billion } | Measure-Object -Sum).Sum
    if ($total -gt $maxHours) { $maxHours = $total }
}

$width = 1550
$height = 940
$left = 92
$top = 165
$barHeight = 78
$barGap = 82
$plotWidth = 990

$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

$bg = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(250, 250, 248))
$axisBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(33, 37, 43))
$mutedBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(87, 92, 101))
$gridPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(220, 224, 227)), 1
$titleFont = New-Object System.Drawing.Font "Segoe UI", 27, ([System.Drawing.FontStyle]::Bold)
$subtitleFont = New-Object System.Drawing.Font "Segoe UI", 15, ([System.Drawing.FontStyle]::Regular)
$axisFont = New-Object System.Drawing.Font "Segoe UI", 12, ([System.Drawing.FontStyle]::Regular)
$labelFont = New-Object System.Drawing.Font "Segoe UI", 13, ([System.Drawing.FontStyle]::Bold)
$smallFont = New-Object System.Drawing.Font "Segoe UI", 11, ([System.Drawing.FontStyle]::Regular)
$legendFont = New-Object System.Drawing.Font "Segoe UI", 10, ([System.Drawing.FontStyle]::Regular)

$g.FillRectangle($bg, 0, 0, $width, $height)
$g.DrawString("AETHER robotics productivity screen", $titleFont, $axisBrush, 64, 42)
$g.DrawString("Useful robot task-hours, fleet stock, replacement flow, and operating cost at 100 GtCO2/year; scenario assumptions, not forecasts.", $subtitleFont, $mutedBrush, 66, 84)

for ($tick = 0; $tick -le [math]::Ceiling($maxHours / 5) * 5; $tick += 5) {
    $x = $left + ($tick / $maxHours) * $plotWidth
    $g.DrawLine($gridPen, [float]$x, [float]($top - 20), [float]$x, [float]($top + 3 * ($barHeight + $barGap) - 28))
    $g.DrawString($tick.ToString("0"), $axisFont, $mutedBrush, [float]($x - 8), [float]($top + 3 * ($barHeight + $barGap) - 18))
}
$g.DrawString("Annual useful robot task-hours, billion", $axisFont, $axisBrush, $left, 640)

for ($i = 0; $i -lt $scenarioOrder.Count; $i++) {
    $scenario = $scenarioOrder[$i]
    $y = $top + $i * ($barHeight + $barGap)
    $g.DrawString($scenarioLabels[$scenario], $labelFont, $axisBrush, $left, [float]($y - 34))
    $x = [double]$left
    foreach ($task in $taskOrder) {
        $row = $taskRows | Where-Object { $_.scenario -eq $scenario -and $_.task_family -eq $task } | Select-Object -First 1
        if ($null -eq $row) { continue }
        $value = [double]$row.annual_useful_task_hours_billion
        $w = ($value / $maxHours) * $plotWidth
        if ($w -gt 0) {
            $brush = New-Object System.Drawing.SolidBrush $colors[$task]
            $g.FillRectangle($brush, [float]$x, [float]$y, [float]$w, [float]$barHeight)
            $brush.Dispose()
            if ($w -gt 56) {
                $g.DrawString($taskLabels[$task], $legendFont, [System.Drawing.Brushes]::White, [float]($x + 7), [float]($y + 28))
            }
            $x += $w
        }
    }

    $summary = $summaryRows | Where-Object { $_.scenario -eq $scenario } | Select-Object -First 1
    $text = "Fleet " + ([double]$summary.robot_stock_required_million).ToString("0.00") + "M | production " + ([double]$summary.annual_robot_production_requirement_robots).ToString("N0") + "/y | cost $" + ([double]$summary.annual_robot_operating_cost_billion_usd).ToString("N0") + "B/y"
    $g.DrawString($text, $smallFont, $mutedBrush, 1115, [float]($y + 20))
}

$legendX = 65
$legendY = 702
$colWidth = 245
for ($i = 0; $i -lt $taskOrder.Count; $i++) {
    $task = $taskOrder[$i]
    $col = $i % 4
    $row = [math]::Floor($i / 4)
    $x = $legendX + $col * $colWidth
    $y = $legendY + $row * 38
    $brush = New-Object System.Drawing.SolidBrush $colors[$task]
    $g.FillRectangle($brush, $x, $y + 4, 22, 14)
    $brush.Dispose()
    $g.DrawString($taskLabels[$task], $legendFont, $axisBrush, $x + 30, $y)
}

$note = "Interpretation: the old robot-count proxy is too crude. The useful variable is task-hours by bottleneck: O&M, storage-field work, construction, MRV, logistics, modules, spares, and R&D. Robots matter if they cut these hours and supervision ratios without weakening safety or verification."
$g.DrawString($note, $subtitleFont, $mutedBrush, (New-Object System.Drawing.RectangleF 64, 820, 1380, 60))
$g.DrawString("Source: aether_robotics_productivity_model.py. Values are scenario assumptions anchored to the robotics evidence map and should be replaced with task-level productivity distributions.", $smallFont, $mutedBrush, 64, 890)

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()

Write-Host "Wrote $Output"

