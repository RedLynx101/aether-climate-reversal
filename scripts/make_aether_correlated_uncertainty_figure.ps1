param(
    [string]$SummaryPath = (Join-Path $PSScriptRoot "..\analysis\tables\aether_correlated_uncertainty_summary.csv"),
    [string]$Output = (Join-Path $PSScriptRoot "..\analysis\figures\correlated_uncertainty_success_frontier.png")
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$rows = @(Import-Csv -LiteralPath $SummaryPath)
$width = 1600
$height = 980
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::FromArgb(248, 248, 246))

$titleFont = New-Object System.Drawing.Font("Segoe UI Semibold", 30)
$subtitleFont = New-Object System.Drawing.Font("Segoe UI", 15)
$axisFont = New-Object System.Drawing.Font("Segoe UI", 12)
$smallFont = New-Object System.Drawing.Font("Segoe UI", 10)
$titleBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(30, 36, 43))
$mutedBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(84, 92, 101))
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(221, 225, 229), 1)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(128, 137, 146), 1)

$colors = @{
    "gross_100_probability" = [System.Drawing.Color]::FromArgb(59, 119, 174)
    "durable_100_probability" = [System.Drawing.Color]::FromArgb(42, 150, 130)
    "positive_climate_reversal_probability" = [System.Drawing.Color]::FromArgb(232, 157, 65)
    "strong_reversal_probability" = [System.Drawing.Color]::FromArgb(181, 81, 78)
}
$metricLabels = @{
    "gross_100_probability" = "Gross >= 100"
    "durable_100_probability" = "Durable >= 100"
    "positive_climate_reversal_probability" = "Net positive"
    "strong_reversal_probability" = "Net >= current emissions"
}
$metrics = @(
    "gross_100_probability",
    "durable_100_probability",
    "positive_climate_reversal_probability",
    "strong_reversal_probability"
)

$g.DrawString("AETHER Correlated Uncertainty Scenario Families", $titleFont, $titleBrush, 54, 34)
$g.DrawString("Pass rates change sharply when clean power, automation, storage/MRV, and rebound assumptions move together.", $subtitleFont, $mutedBrush, 56, 86)

$plotX = 330
$plotY = 168
$plotW = 1120
$rowH = 88
$barH = 12
$metricGap = 8

for ($tick = 0; $tick -le 100; $tick += 20) {
    $x = $plotX + ($tick / 100.0) * $plotW
    $g.DrawLine($gridPen, [float]$x, [float]($plotY - 20), [float]$x, [float]($plotY + $rowH * $rows.Count - 12))
    $g.DrawString("$tick%", $smallFont, $mutedBrush, [float]($x - 13), [float]($plotY + $rowH * $rows.Count))
}
$g.DrawLine($axisPen, $plotX, $plotY - 20, $plotX, $plotY + $rowH * $rows.Count - 12)

for ($i = 0; $i -lt $rows.Count; $i++) {
    $row = $rows[$i]
    $y = $plotY + $i * $rowH
    $g.DrawString($row.label, $axisFont, $titleBrush, 54, [float]($y + 13))
    $g.DrawString(("Primary: " + $row.primary_binding_constraint), $smallFont, $mutedBrush, 56, [float]($y + 38))
    for ($j = 0; $j -lt $metrics.Count; $j++) {
        $metric = $metrics[$j]
        $value = [double]$row.$metric
        $barY = $y + 8 + $j * ($barH + $metricGap)
        $barW = [Math]::Max(1.0, $value * $plotW)
        $brush = New-Object System.Drawing.SolidBrush($colors[$metric])
        $g.FillRectangle($brush, [float]$plotX, [float]$barY, [float]$barW, [float]$barH)
        $brush.Dispose()
        $label = ($value * 100.0).ToString("0.0") + "%"
        $labelX = [Math]::Min($plotX + $barW + 8, $plotX + $plotW + 8)
        $g.DrawString($label, $smallFont, $mutedBrush, [float]$labelX, [float]($barY - 4))
    }
}

$legendX = 54
$legendY = 812
for ($j = 0; $j -lt $metrics.Count; $j++) {
    $metric = $metrics[$j]
    $brush = New-Object System.Drawing.SolidBrush($colors[$metric])
    $x = $legendX + $j * 330
    $g.FillRectangle($brush, $x, $legendY, 18, 12)
    $brush.Dispose()
    $g.DrawString($metricLabels[$metric], $smallFont, $mutedBrush, $x + 26, $legendY - 4)
}

$note = "Interpretation: these are scenario-family sensitivities, not calibrated probabilities. The useful result is the dependency structure: AETHER only looks strong when clean power, automation, storage/MRV, rebound control, and execution improve together."
$g.DrawString($note, $subtitleFont, $mutedBrush, (New-Object System.Drawing.RectangleF 56, 856, 1450, 58))
$g.DrawString("Source: aether_correlated_uncertainty_model.py, using the current uncertainty distribution registry and the same physical capacity equations as the independent Monte Carlo screen.", $smallFont, $mutedBrush, 56, 932)

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()

Write-Host "Wrote $Output"

