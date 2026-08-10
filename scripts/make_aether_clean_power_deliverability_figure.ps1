param(
    [string]$CasesPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "analysis\tables\aether_clean_power_deliverability_cases.csv"),
    [string]$Output = (Join-Path (Split-Path -Parent $PSScriptRoot) "analysis\figures\clean_power_deliverability_gate.png")
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$rows = @(Import-Csv -LiteralPath $CasesPath)
$width = 1600
$height = 980
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::FromArgb(249, 249, 247))

$titleFont = New-Object System.Drawing.Font("Segoe UI Semibold", 30)
$subtitleFont = New-Object System.Drawing.Font("Segoe UI", 15)
$labelFont = New-Object System.Drawing.Font("Segoe UI Semibold", 12)
$smallFont = New-Object System.Drawing.Font("Segoe UI", 9)
$axisFont = New-Object System.Drawing.Font("Segoe UI", 11)
$titleBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(28, 35, 43))
$mutedBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(82, 91, 101))
$barBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(54, 139, 143))
$passBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(72, 154, 94))
$failBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(188, 78, 69))
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(218, 222, 224), 1)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(119, 127, 135), 1)
$targetPen50 = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(230, 151, 56), 2)
$targetPen100 = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(174, 61, 61), 2)
$targetPen100.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
$noteFormat = New-Object System.Drawing.StringFormat
$noteFormat.Trimming = [System.Drawing.StringTrimming]::EllipsisWord

$g.DrawString("P0 F2 Clean-Power Deliverability Gate", $titleFont, $titleBrush, 56, 42)
$g.DrawString("Delivered additional clean power after ordinary demand, interconnection, transmission, hourly matching, firming, and additionality.", $subtitleFont, $mutedBrush, 58, 88)

$labelX = 60
$plotX = 500
$plotY = 190
$plotW = 860
$rowH = 86
$barH = 28
$maxGt = 160.0

foreach ($tick in @(0, 25, 50, 75, 100, 125, 150)) {
    $x = $plotX + ($tick / $maxGt) * $plotW
    $g.DrawLine($gridPen, [float]$x, [float]($plotY - 22), [float]$x, [float]($plotY + $rows.Count * $rowH - 18))
    $g.DrawString([string]$tick, $axisFont, $mutedBrush, [float]($x - 8), [float]($plotY - 37))
}
$g.DrawString("Maximum GtCO2/year powered at 3 GJ/tCO2", $axisFont, $mutedBrush, $plotX, 138)

$x50 = $plotX + (50.0 / $maxGt) * $plotW
$x100 = $plotX + (100.0 / $maxGt) * $plotW
$g.DrawLine($targetPen50, [float]$x50, [float]($plotY - 18), [float]$x50, [float]($plotY + $rows.Count * $rowH - 18))
$g.DrawLine($targetPen100, [float]$x100, [float]($plotY - 18), [float]$x100, [float]($plotY + $rows.Count * $rowH - 18))

for ($i = 0; $i -lt $rows.Count; $i++) {
    $row = $rows[$i]
    $y = $plotY + $i * $rowH
    $label = [string]$row.display_name
    $rule = [string]$row.paper_use_rule
    $max = [double]$row.max_gtco2_y_at_3gj_balanced_gate
    $barW = [Math]::Max(2.0, ($max / $maxGt) * $plotW)
    $g.DrawString($label, $labelFont, $titleBrush, $labelX, $y)
    $g.DrawString($rule, $smallFont, $mutedBrush, (New-Object System.Drawing.RectangleF $labelX, ($y + 24), ($plotX - $labelX - 28), 42), $noteFormat)
    $brush = if ($max -ge 100.0) { $passBrush } else { $barBrush }
    $g.FillRectangle($brush, [float]$plotX, [float]($y + 12), [float]$barW, [float]$barH)
    $valueX = if ($barW -lt 44) { $plotX + 52 } else { $plotX + $barW + 8 }
    $g.DrawString($max.ToString("0.0") + " Gt/y", $smallFont, $titleBrush, [float]$valueX, [float]($y + 17))
}

$legendX = 1390
$g.DrawLine($axisPen, $legendX - 25, 186, $legendX - 25, 706)
$g.DrawString("Targets", $labelFont, $titleBrush, $legendX, 190)
$g.DrawLine($targetPen50, $legendX, 238, $legendX + 86, 238)
$g.DrawString("50 Gt/y", $smallFont, $titleBrush, $legendX, 252)
$g.DrawLine($targetPen100, $legendX, 306, $legendX + 86, 306)
$g.DrawString("100 Gt/y", $smallFont, $titleBrush, $legendX, 320)
$g.FillRectangle($passBrush, $legendX, 388, 86, 12)
$g.DrawString("passes 100", $smallFont, $titleBrush, $legendX, 404)
$g.FillRectangle($barBrush, $legendX, 456, 86, 12)
$g.DrawString("does not pass", $smallFont, $titleBrush, $legendX, 472)

$note = "Interpretation: cheap clean energy helps, but annual TWh is not the same as delivered additional industrial power. In this screen, only the upper-tail abundance case clears the 100 Gt/y clean-power gate."
$g.DrawString($note, $subtitleFont, $mutedBrush, (New-Object System.Drawing.RectangleF 58, 796, 1450, 62))
$g.DrawString("Source: aether_clean_power_deliverability_model.py. Scenario factors are explicit F2 gate assumptions anchored to IEA, IRENA, NREL, Berkeley Lab, EIA, CEC, and AETHER clean-power outputs.", $smallFont, $mutedBrush, 58, 914)

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()
Write-Host "Wrote $Output"

