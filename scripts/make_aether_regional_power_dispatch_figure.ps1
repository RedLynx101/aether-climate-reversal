param(
    [string]$CasesPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "analysis\tables\aether_regional_power_dispatch_cases.csv"),
    [string]$Output = (Join-Path (Split-Path -Parent $PSScriptRoot) "analysis\figures\regional_power_dispatch_gate.png")
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$rows = @(Import-Csv -LiteralPath $CasesPath)
$width = 1600
$height = 930
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::FromArgb(250, 249, 246))

$titleFont = New-Object System.Drawing.Font("Segoe UI Semibold", 30)
$subtitleFont = New-Object System.Drawing.Font("Segoe UI", 15)
$labelFont = New-Object System.Drawing.Font("Segoe UI Semibold", 12)
$smallFont = New-Object System.Drawing.Font("Segoe UI", 9)
$axisFont = New-Object System.Drawing.Font("Segoe UI", 11)
$titleBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(28, 35, 43))
$mutedBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(80, 88, 96))
$barBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(53, 126, 137))
$passBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(67, 143, 87))
$failBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(184, 77, 70))
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(220, 224, 226), 1)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(120, 128, 136), 1)
$targetPen50 = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(190, 120, 55), 2)
$targetPen100 = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(170, 45, 48), 3)
$targetPen50.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
$targetPen100.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash

$g.DrawString("AETHER regional clean-power dispatch gate", $titleFont, $titleBrush, 60, 40)
$g.DrawString("Representative-day regional screen: delivered additional power after ordinary demand, grid delivery, storage, hourly matching, and colocation constraints", $subtitleFont, $mutedBrush, 62, 88)

$plotLeft = 360
$plotRight = 1460
$plotTop = 170
$plotBottom = 760
$xMax = 130.0
$plotWidth = $plotRight - $plotLeft

foreach ($tick in 0, 25, 50, 75, 100, 125) {
    $x = $plotLeft + ($tick / $xMax) * $plotWidth
    $g.DrawLine($gridPen, [int]$x, $plotTop, [int]$x, $plotBottom)
    $g.DrawString([string]$tick, $axisFont, $mutedBrush, [int]($x - 10), $plotBottom + 16)
}
$x50 = $plotLeft + (50.0 / $xMax) * $plotWidth
$x100 = $plotLeft + (100.0 / $xMax) * $plotWidth
$g.DrawLine($targetPen50, [int]$x50, $plotTop - 10, [int]$x50, $plotBottom)
$g.DrawLine($targetPen100, [int]$x100, $plotTop - 10, [int]$x100, $plotBottom)
$g.DrawString("50 Gt/y", $smallFont, $mutedBrush, [int]($x50 + 8), $plotTop - 32)
$g.DrawString("100 Gt/y", $smallFont, $mutedBrush, [int]($x100 + 8), $plotTop - 32)

$rowGap = 26
$barHeight = 52
$y = $plotTop + 18
$ordered = $rows | Sort-Object {[double]$_.max_gtco2_y_supported}
foreach ($row in $ordered) {
    $value = [double]$row.max_gtco2_y_supported
    $barWidth = [Math]::Max(2, ($value / $xMax) * $plotWidth)
    $brush = if ($row.passes_100gt -eq "True") { $passBrush } else { $barBrush }
    $g.DrawString($row.display_name, $labelFont, $titleBrush, 60, [int]($y + 13))
    $g.FillRectangle($brush, $plotLeft, [int]$y, [int]$barWidth, $barHeight)
    $g.DrawRectangle($axisPen, $plotLeft, [int]$y, [int]$barWidth, $barHeight)
    $valueLabel = $value.ToString("0.0") + " GtCO2/y"
    $g.DrawString($valueLabel, $labelFont, $titleBrush, [int]($plotLeft + $barWidth + 12), [int]($y + 14))
    $match = ([double]$row.weighted_hourly_match_share * 100.0).ToString("0")
    $score = ([double]$row.weighted_colocation_score).ToString("0.00")
    $statusBrush = if ($row.passes_100gt -eq "True") { $passBrush } else { $failBrush }
    $status = if ($row.passes_100gt -eq "True") { "passes 100 Gt/y" } else { "fails 100 Gt/y" }
    $g.DrawString("$match% hourly match, colocation score $score, $status", $smallFont, $statusBrush, 60, [int]($y + 35))
    $y += $barHeight + $rowGap
}

$g.DrawLine($axisPen, $plotLeft, $plotBottom, $plotRight, $plotBottom)
$g.DrawString("Supported AETHER gross removal at 3 GJ/tCO2 with delivered regional power (GtCO2/year)", $axisFont, $mutedBrush, $plotLeft + 230, $plotBottom + 46)

$noteTop = 815
$g.DrawString("Read as a screen, not a power-market simulation.", $labelFont, $titleBrush, 60, $noteTop)
$g.DrawString("The model uses regional archetypes and a 24-hour representative-day dispatch. It is designed to stop annual TWh optimism from substituting for delivered industrial power.", $smallFont, $mutedBrush, 60, $noteTop + 28)

$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()
Write-Host "Wrote $Output"

