$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$TableDir = Join-Path $Root "analysis\tables"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null

function Save-Png($Bitmap, [string]$Path) {
    $ms = New-Object System.IO.MemoryStream
    $Bitmap.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
    [System.IO.File]::WriteAllBytes($Path, $ms.ToArray())
    $ms.Dispose()
}

function Draw-LineChart($g, $Rows, [string]$YField, [double]$YMin, [double]$YMax, [int]$Left, [int]$Top, [int]$Width, [int]$Height, [string]$Title, [string]$YAxisLabel) {
    $axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(85,85,85), 2)
    $gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(220,220,215), 1)
    $titleFont = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
    $labelFont = New-Object System.Drawing.Font("Arial", 11)
    $g.DrawString($Title, $titleFont, [System.Drawing.Brushes]::Black, $Left, $Top - 34)
    $g.DrawRectangle($axisPen, $Left, $Top, $Width, $Height)
    for ($i = 0; $i -le 4; $i++) {
        $y = $Top + $Height - ($Height * $i / 4)
        $value = $YMin + (($YMax - $YMin) * $i / 4)
        $g.DrawLine($gridPen, $Left, $y, $Left + $Width, $y)
        $g.DrawString($value.ToString("0"), $labelFont, [System.Drawing.Brushes]::DimGray, $Left - 52, $y - 8)
    }
    foreach ($year in @(2026, 2030, 2040, 2050, 2060)) {
        $x = $Left + (($year - 2026) / 34.0) * $Width
        $g.DrawLine($gridPen, $x, $Top, $x, $Top + $Height)
        $g.DrawString([string]$year, $labelFont, [System.Drawing.Brushes]::DimGray, $x - 18, $Top + $Height + 10)
    }
    $g.DrawString($YAxisLabel, $labelFont, [System.Drawing.Brushes]::DimGray, $Left - 58, $Top - 22)
    $axisPen.Dispose(); $gridPen.Dispose(); $titleFont.Dispose(); $labelFont.Dispose()
}

function Plot-Series($g, $Rows, [string]$YField, [double]$YMin, [double]$YMax, [int]$Left, [int]$Top, [int]$Width, [int]$Height, [System.Drawing.Color]$Color) {
    $pen = New-Object System.Drawing.Pen($Color, 4)
    $points = New-Object System.Collections.Generic.List[System.Drawing.PointF]
    foreach ($row in ($Rows | Sort-Object {[int]$_.year})) {
        $year = [int]$row.year
        $value = [double]$row.$YField
        $x = $Left + (($year - 2026) / 34.0) * $Width
        $y = $Top + $Height - (($value - $YMin) / ($YMax - $YMin)) * $Height
        $points.Add([System.Drawing.PointF]::new([float]$x, [float]$y))
    }
    if ($points.Count -gt 1) {
        $g.DrawLines($pen, $points.ToArray())
    }
    $pen.Dispose()
}

$rows = Import-Csv (Join-Path $TableDir "aether_deployment_timepath_annual.csv")
$summary = Import-Csv (Join-Path $TableDir "aether_deployment_timepath_summary.csv")
$selected = @("linear_reference_2046", "s_curve_industrialization", "abundance_acceleration_2040", "energy_delayed", "rebound_failure")
$colors = @{
    linear_reference_2046 = [System.Drawing.Color]::FromArgb(42, 104, 130)
    s_curve_industrialization = [System.Drawing.Color]::FromArgb(70, 145, 105)
    abundance_acceleration_2040 = [System.Drawing.Color]::FromArgb(129, 99, 166)
    energy_delayed = [System.Drawing.Color]::FromArgb(196, 128, 47)
    rebound_failure = [System.Drawing.Color]::FromArgb(171, 82, 75)
}

$bmp = New-Object System.Drawing.Bitmap 1700, 1100
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(250,250,248))

$titleFont = New-Object System.Drawing.Font("Arial", 30, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 16)
$g.DrawString("AETHER Deployment Timepaths", $titleFont, [System.Drawing.Brushes]::Black, 70, 44)
$g.DrawString("Annual gross removal and cumulative durable credit under explicit 2026-2060 scenario assumptions.", $subFont, [System.Drawing.Brushes]::DimGray, 72, 90)

Draw-LineChart $g $rows "actual_gross_removal_gtco2_y" 0 110 105 180 690 325 "Annual gross removal" "GtCO2/y"
$durableMax = [double](($rows | Measure-Object cumulative_durable_credit_gtco2 -Maximum).Maximum)
$durableAxis = [Math]::Ceiling($durableMax / 500.0) * 500.0
Draw-LineChart $g $rows "cumulative_durable_credit_gtco2" 0 $durableAxis 105 635 690 325 "Cumulative durable credited removal" "GtCO2"

$legendFont = New-Object System.Drawing.Font("Arial", 13)
$smallFont = New-Object System.Drawing.Font("Arial", 12)
$xLegend = 870
$yLegend = 180
foreach ($scenario in $selected) {
    $series = @($rows | Where-Object { $_.scenario -eq $scenario })
    Plot-Series $g $series "actual_gross_removal_gtco2_y" 0 110 105 180 690 325 $colors[$scenario]
    Plot-Series $g $series "cumulative_durable_credit_gtco2" 0 $durableAxis 105 635 690 325 $colors[$scenario]
    $brush = New-Object System.Drawing.SolidBrush($colors[$scenario])
    $g.FillRectangle($brush, $xLegend, $yLegend, 22, 12)
    $name = ($summary | Where-Object { $_.scenario -eq $scenario } | Select-Object -First 1).display_name
    $g.DrawString($name, $legendFont, [System.Drawing.Brushes]::Black, $xLegend + 34, $yLegend - 6)
    $brush.Dispose()
    $yLegend += 34
}

$calloutFont = New-Object System.Drawing.Font("Arial", 14)
$calloutBold = New-Object System.Drawing.Font("Arial", 14, [System.Drawing.FontStyle]::Bold)
$g.DrawString("Read this as a constraint screen, not a forecast.", $calloutBold, [System.Drawing.Brushes]::Black, 870, 390)
$callouts = @(
    "The 100 Gt/y target is annual capacity; climate value depends on cumulative durable credit.",
    "Energy-delayed cases miss the target even when robotics assumptions remain optimistic.",
    "High rebound can leave the physical system impressive while the net-climate result fails.",
    "A publishable version needs regional buildout, storage basins, LCA, and correlated uncertainty."
)
$yCallout = 430
foreach ($text in $callouts) {
    $g.DrawString($text, $calloutFont, [System.Drawing.Brushes]::DimGray, 870, $yCallout)
    $yCallout += 42
}

$footerFont = New-Object System.Drawing.Font("Arial", 11)
$g.DrawString("Source: aether_deployment_timepath_model.py and generated deployment CSVs. Scenario assumptions are explicit AETHER screens, not forecasts.", $footerFont, [System.Drawing.Brushes]::DimGray, 70, 1040)

Save-Png $bmp (Join-Path $FigureDir "deployment_timepath_capacity_and_cumulative.png")

$titleFont.Dispose(); $subFont.Dispose(); $legendFont.Dispose(); $smallFont.Dispose(); $calloutFont.Dispose(); $calloutBold.Dispose(); $footerFont.Dispose(); $g.Dispose(); $bmp.Dispose()

