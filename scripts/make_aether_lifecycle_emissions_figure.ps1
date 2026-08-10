$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$Table = Join-Path $Root "analysis\tables\aether_lifecycle_emissions_summary.csv"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null
$OutPath = Join-Path $FigureDir "lifecycle_emissions_net_credit_sensitivity.png"

function Save-Png($Bitmap, [string]$Path) {
    $ms = New-Object System.IO.MemoryStream
    try {
        $Bitmap.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
        [System.IO.File]::WriteAllBytes($Path, $ms.ToArray())
    }
    finally {
        $ms.Dispose()
    }
}

function Draw-Text($Graphics, [string]$Text, [System.Drawing.Font]$Font, [System.Drawing.Brush]$Brush, [float]$X, [float]$Y) {
    $Graphics.DrawString($Text, $Font, $Brush, [System.Drawing.PointF]::new($X, $Y))
}

$rows = @(Import-Csv $Table)
$order = @("near_zero_clean_power", "low_carbon_mixed_power", "grid_leakage_case", "fossil_contaminated_case")
$labels = @{
    "near_zero_clean_power" = "5 kg/MWh"
    "low_carbon_mixed_power" = "25 kg/MWh"
    "grid_leakage_case" = "100 kg/MWh"
    "fossil_contaminated_case" = "250 kg/MWh"
}

$width = 1680
$height = 960
$bmp = [System.Drawing.Bitmap]::new($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(249, 249, 246))

$titleFont = [System.Drawing.Font]::new("Arial", 30, [System.Drawing.FontStyle]::Bold)
$subFont = [System.Drawing.Font]::new("Arial", 15)
$axisFont = [System.Drawing.Font]::new("Arial", 12)
$labelFont = [System.Drawing.Font]::new("Arial", 12)
$boldFont = [System.Drawing.Font]::new("Arial", 12, [System.Drawing.FontStyle]::Bold)
$footerFont = [System.Drawing.Font]::new("Arial", 10)
$black = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(24, 24, 24))
$muted = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(82, 82, 82))
$emissionsBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(181, 82, 72))
$durableBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(74, 134, 105))
$creditBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(56, 109, 142))
$gridPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(222, 222, 216), 1)
$axisPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(85, 85, 85), 2)

Draw-Text $g "AETHER Lifecycle Emissions and Creditable Removal" $titleFont $black 64 42
Draw-Text $g "Pathway placeholder LCA plus power-emissions cases; compares gross, lifecycle emissions, durable credit, and MRV-filtered creditable removal." $subFont $muted 66 88

$left = 130
$top = 170
$plotW = 1140
$plotH = 610
$maxY = 110.0

for ($tick = 0; $tick -le 100; $tick += 20) {
    $y = $top + $plotH - ($plotH * $tick / $maxY)
    $g.DrawLine($gridPen, $left, $y, $left + $plotW, $y)
    Draw-Text $g ([string]$tick) $axisFont $muted 82 ($y - 8)
}
$g.DrawLine($axisPen, $left, $top, $left, $top + $plotH)
$g.DrawLine($axisPen, $left, $top + $plotH, $left + $plotW, $top + $plotH)
Draw-Text $g "GtCO2e or GtCO2/year" $axisFont $muted 72 136

$groupW = $plotW / $order.Count
$barW = 46
for ($i = 0; $i -lt $order.Count; $i++) {
    $case = $order[$i]
    $row = @($rows | Where-Object { $_.power_case -eq $case })[0]
    $x0 = $left + $i * $groupW + 44
    $values = @(
        @{label="LCA emissions"; value=[double]$row.annual_lifecycle_emissions_gtco2e_y; brush=$emissionsBrush},
        @{label="Durable after LCA"; value=[double]$row.durable_after_lca_100y_gtco2_y; brush=$durableBrush},
        @{label="Creditable after LCA+MRV"; value=[double]$row.creditable_after_lca_and_mrv_gtco2_y; brush=$creditBrush}
    )
    for ($j = 0; $j -lt $values.Count; $j++) {
        $value = $values[$j].value
        $barH = $plotH * $value / $maxY
        $x = $x0 + $j * ($barW + 18)
        $y = $top + $plotH - $barH
        $g.FillRectangle($values[$j].brush, [float]$x, [float]$y, $barW, [float]$barH)
        Draw-Text $g ($value.ToString("0.0")) $labelFont $black ($x - 1) ($y - 24)
    }
    Draw-Text $g $labels[$case] $boldFont $black ($x0 + 18) ($top + $plotH + 18)
    Draw-Text $g "power emissions" $labelFont $muted ($x0 - 6) ($top + $plotH + 42)
}

$legendX = 1310
$legendY = 220
$g.FillRectangle($emissionsBrush, $legendX, $legendY, 28, 14)
Draw-Text $g "Lifecycle emissions" $labelFont $black ($legendX + 40) ($legendY - 5)
$g.FillRectangle($durableBrush, $legendX, $legendY + 42, 28, 14)
Draw-Text $g "Durable after LCA" $labelFont $black ($legendX + 40) ($legendY + 37)
$g.FillRectangle($creditBrush, $legendX, $legendY + 84, 28, 14)
Draw-Text $g "Creditable after LCA+MRV" $labelFont $black ($legendX + 40) ($legendY + 79)

Draw-Text $g "Read: 100 Gt/y gross only works" $labelFont $muted 1310 405
Draw-Text $g "with additional low-carbon power" $labelFont $muted 1310 429
Draw-Text $g "and controlled non-power LCA." $labelFont $muted 1310 453
Draw-Text $g "Placeholder LCAs only;" $labelFont $muted 1310 510
Draw-Text $g "replace before publication claims." $labelFont $muted 1310 534

Draw-Text $g "Source: aether_lifecycle_emissions_model.py. Next step: replace placeholder intensities with pathway-specific LCA datasets, embodied-emissions factors, and regional supply chains." $footerFont $muted 64 ($height - 48)

Save-Png $bmp $OutPath

$titleFont.Dispose(); $subFont.Dispose(); $axisFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$black.Dispose(); $muted.Dispose(); $emissionsBrush.Dispose(); $durableBrush.Dispose(); $creditBrush.Dispose(); $gridPen.Dispose(); $axisPen.Dispose()
$g.Dispose(); $bmp.Dispose()

Get-Item -LiteralPath $OutPath | Select-Object FullName, Length, LastWriteTime

