$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$ScenarioTable = Join-Path $Root "analysis\tables\aether_integrated_feasibility_scenarios.csv"
$TimeTable = Join-Path $Root "analysis\tables\aether_integrated_feasibility_timepaths.csv"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null

function Save-Png($Bitmap, [string]$Path) {
    $ms = New-Object System.IO.MemoryStream
    $Bitmap.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
    [System.IO.File]::WriteAllBytes($Path, $ms.ToArray())
    $ms.Dispose()
}

function Ratio-Color([double]$Value) {
    if ($Value -ge 1.0) { return [System.Drawing.Color]::FromArgb(83, 133, 105) }
    if ($Value -ge 0.5) { return [System.Drawing.Color]::FromArgb(217, 166, 83) }
    return [System.Drawing.Color]::FromArgb(190, 86, 74)
}

$scenarios = @(Import-Csv $ScenarioTable)
$metrics = @(
    @{ key = "energy_adequacy_ratio"; label = "Energy" },
    @{ key = "robot_adequacy_ratio"; label = "Robots" },
    @{ key = "storage_adequacy_ratio"; label = "Storage" },
    @{ key = "budget_adequacy_ratio"; label = "Budget" },
    @{ key = "terminal_capacity_ratio"; label = "Capacity" },
    @{ key = "net_target_ratio_vs_current_emissions"; label = "Net" }
)

$width = 1500
$height = 900
$bmp = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(250,250,248))

$titleFont = New-Object System.Drawing.Font("Arial", 29, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 15)
$labelFont = New-Object System.Drawing.Font("Arial", 13)
$labelBold = New-Object System.Drawing.Font("Arial", 13, [System.Drawing.FontStyle]::Bold)
$smallFont = New-Object System.Drawing.Font("Arial", 10)
$footerFont = New-Object System.Drawing.Font("Arial", 10)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(210,210,205), 1)
$borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(120,120,115), 1)

$g.DrawString("AETHER Integrated Feasibility Screen", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("Resource adequacy ratios at the 2046 100 GtCO2/year target. Values below 1.0 identify binding constraints.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 410
$top = 165
$cellW = 155
$cellH = 70
$rowGap = 16

for ($m = 0; $m -lt $metrics.Count; $m++) {
    $x = $left + $m * $cellW
    $g.DrawString($metrics[$m].label, $labelBold, [System.Drawing.Brushes]::Black, $x + 24, $top - 38)
}

for ($i = 0; $i -lt $scenarios.Count; $i++) {
    $s = $scenarios[$i]
    $y = $top + $i * ($cellH + $rowGap)
    $g.DrawString([string]$s.display_name, $labelBold, [System.Drawing.Brushes]::Black, 64, $y + 6)
    $screenLabel = ([string]$s.screen_result).Replace("_", " ")
    $g.DrawString($screenLabel, $smallFont, [System.Drawing.Brushes]::DimGray, 66, $y + 31)
    for ($m = 0; $m -lt $metrics.Count; $m++) {
        $metric = $metrics[$m].key
        $value = [double]$s.$metric
        $x = $left + $m * $cellW
        $brush = New-Object System.Drawing.SolidBrush (Ratio-Color $value)
        $g.FillRectangle($brush, $x, $y, $cellW - 12, $cellH)
        $g.DrawRectangle($borderPen, $x, $y, $cellW - 12, $cellH)
        $text = if ($value -ge 10) { $value.ToString("0.0") + "x" } else { $value.ToString("0.00") + "x" }
        $g.DrawString($text, $labelBold, [System.Drawing.Brushes]::White, $x + 38, $y + 22)
        $brush.Dispose()
    }
}

$legendY = 730
$legend = @(
    @{ text = ">= 1.0 passes screen"; color = [System.Drawing.Color]::FromArgb(83, 133, 105) },
    @{ text = "0.5-1.0 constrained"; color = [System.Drawing.Color]::FromArgb(217, 166, 83) },
    @{ text = "< 0.5 severe gap"; color = [System.Drawing.Color]::FromArgb(190, 86, 74) }
)
for ($i = 0; $i -lt $legend.Count; $i++) {
    $x = 66 + $i * 285
    $brush = New-Object System.Drawing.SolidBrush $legend[$i].color
    $g.FillRectangle($brush, $x, $legendY, 28, 16)
    $g.DrawString($legend[$i].text, $labelFont, [System.Drawing.Brushes]::Black, $x + 38, $legendY - 4)
    $brush.Dispose()
}
$g.DrawString("Net ratio compares net removal at 100 GtCO2/year against the 57.8 Gt/year net-negative benchmark from current emissions.", $smallFont, [System.Drawing.Brushes]::DimGray, 66, 786)
$g.DrawString("Source: aether_integrated_feasibility_model.py", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 44)

Save-Png $bmp (Join-Path $FigureDir "integrated_feasibility_screen_2046.png")
$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $labelBold.Dispose(); $smallFont.Dispose(); $footerFont.Dispose(); $gridPen.Dispose(); $borderPen.Dispose(); $g.Dispose(); $bmp.Dispose()

$timeRows = @(Import-Csv $TimeTable)
$width = 1500
$height = 900
$bmp = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(250,250,248))

$titleFont = New-Object System.Drawing.Font("Arial", 29, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 15)
$axisFont = New-Object System.Drawing.Font("Arial", 12)
$legendFont = New-Object System.Drawing.Font("Arial", 10)
$footerFont = New-Object System.Drawing.Font("Arial", 10)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(85,85,85), 2)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(222,222,216), 1)

$g.DrawString("AETHER Capacity Paths Under Integrated Constraints", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("Actual removal capacity is the minimum of target schedule, clean energy, robot supply, storage, and budget capacity.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$plotLeft = 105
$plotTop = 150
$plotW = 1000
$plotH = 575
$maxY = 110.0
$startYear = 2026
$endYear = 2046

for ($i = 0; $i -le 5; $i++) {
    $yVal = $maxY * $i / 5
    $y = $plotTop + $plotH - ($plotH * $yVal / $maxY)
    $g.DrawLine($gridPen, $plotLeft, $y, $plotLeft + $plotW, $y)
    $g.DrawString(([int]$yVal).ToString(), $axisFont, [System.Drawing.Brushes]::DimGray, 62, $y - 9)
}
for ($i = 0; $i -le 4; $i++) {
    $year = $startYear + [int](($endYear - $startYear) * $i / 4)
    $x = $plotLeft + $plotW * ($year - $startYear) / ($endYear - $startYear)
    $g.DrawLine($gridPen, $x, $plotTop, $x, $plotTop + $plotH)
    $g.DrawString($year.ToString(), $axisFont, [System.Drawing.Brushes]::DimGray, $x - 22, $plotTop + $plotH + 14)
}
$g.DrawLine($axisPen, $plotLeft, $plotTop, $plotLeft, $plotTop + $plotH)
$g.DrawLine($axisPen, $plotLeft, $plotTop + $plotH, $plotLeft + $plotW, $plotTop + $plotH)

$colorMap = @{
    "reference_extrapolation" = [System.Drawing.Color]::FromArgb(165, 85, 73)
    "fast_learning_energy_constrained" = [System.Drawing.Color]::FromArgb(214, 145, 54)
    "aether_portfolio_push" = [System.Drawing.Color]::FromArgb(42, 104, 130)
    "moonshot_low_energy" = [System.Drawing.Color]::FromArgb(76, 137, 89)
    "rebound_failure" = [System.Drawing.Color]::FromArgb(120, 95, 150)
}

$grouped = $timeRows | Group-Object scenario
$legendX = 1160
$legendY = 170
foreach ($group in $grouped) {
    $rows = @($group.Group | Sort-Object {[int]$_.year})
    $color = $colorMap[$group.Name]
    $pen = New-Object System.Drawing.Pen($color, 4)
    for ($i = 1; $i -lt $rows.Count; $i++) {
        $prev = $rows[$i - 1]
        $curr = $rows[$i]
        $x1 = $plotLeft + $plotW * (([int]$prev.year - $startYear) / ($endYear - $startYear))
        $y1 = $plotTop + $plotH - ($plotH * ([double]$prev.actual_capacity_gtco2_y) / $maxY)
        $x2 = $plotLeft + $plotW * (([int]$curr.year - $startYear) / ($endYear - $startYear))
        $y2 = $plotTop + $plotH - ($plotH * ([double]$curr.actual_capacity_gtco2_y) / $maxY)
        $g.DrawLine($pen, $x1, $y1, $x2, $y2)
    }
    $brush = New-Object System.Drawing.SolidBrush $color
    $legendRow = $scenarios | Where-Object { $_.scenario -eq $group.Name } | Select-Object -First 1
    $g.FillRectangle($brush, $legendX, $legendY, 28, 13)
    $g.DrawString([string]$legendRow.display_name, $legendFont, [System.Drawing.Brushes]::Black, $legendX + 38, $legendY - 5)
    $legendY += 38
    $brush.Dispose()
    $pen.Dispose()
}
$targetPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(70,70,70), 2)
$targetPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
$g.DrawLine($targetPen, $plotLeft, $plotTop + $plotH, $plotLeft + $plotW, $plotTop + $plotH - ($plotH * 100 / $maxY))
$g.DrawString("Linear 100 Gt/y target", $legendFont, [System.Drawing.Brushes]::DimGray, $legendX, $legendY + 8)
$g.DrawString("GtCO2/year removal capacity", $axisFont, [System.Drawing.Brushes]::DimGray, 60, 125)
$g.DrawString("Source: aether_integrated_feasibility_model.py", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 44)

Save-Png $bmp (Join-Path $FigureDir "integrated_capacity_paths_2026_2046.png")
$titleFont.Dispose(); $subFont.Dispose(); $axisFont.Dispose(); $legendFont.Dispose(); $footerFont.Dispose()
$axisPen.Dispose(); $gridPen.Dispose(); $targetPen.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "integrated_feasibility_screen_2046.png"), (Join-Path $FigureDir "integrated_capacity_paths_2026_2046.png") | Select-Object FullName,Length
