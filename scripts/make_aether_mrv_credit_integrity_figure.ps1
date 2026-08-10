$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$TableDir = Join-Path $Root "analysis\tables"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null

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

$rows = @(Import-Csv (Join-Path $TableDir "aether_mrv_credit_integrity_by_pathway.csv") |
    Sort-Object {[double]$_.creditable_fraction_of_gross} -Descending)
$summary = @{}
Import-Csv (Join-Path $TableDir "aether_mrv_credit_integrity_summary.csv") | ForEach-Object {
    $summary[$_.summary_id] = $_.value
}

$width = 1900
$height = 980
$bmp = [System.Drawing.Bitmap]::new($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(248, 248, 244))

$fontTitle = [System.Drawing.Font]::new("Arial", 34, [System.Drawing.FontStyle]::Bold)
$fontSubtitle = [System.Drawing.Font]::new("Arial", 16, [System.Drawing.FontStyle]::Regular)
$fontLabel = [System.Drawing.Font]::new("Arial", 13, [System.Drawing.FontStyle]::Bold)
$fontSmall = [System.Drawing.Font]::new("Arial", 10, [System.Drawing.FontStyle]::Regular)
$fontValue = [System.Drawing.Font]::new("Arial", 13, [System.Drawing.FontStyle]::Regular)
$fontFooter = [System.Drawing.Font]::new("Arial", 11, [System.Drawing.FontStyle]::Regular)

$black = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(20, 20, 20))
$muted = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(85, 85, 85))
$gridPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(215, 215, 208), 1)
$axisPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(70, 70, 70), 2)

Draw-Text $g "AETHER MRV and Credit-Integrity Filter" $fontTitle $black 64 42
Draw-Text $g "Gross, durable, and creditable tonnes diverge. Provisional buffers turn 100 GtCO2/y gross into $($summary["mrv_creditable_total"]) GtCO2/y creditable removal." $fontSubtitle $muted 64 88

$leftLabel = 64
$plotLeft = 520
$plotTop = 145
$plotWidth = 930
$barHeight = 40
$rowGap = 36
$maxFraction = 1.0

foreach ($tick in @(0, 0.25, 0.5, 0.75, 1.0)) {
    $x = $plotLeft + [int]($plotWidth * $tick / $maxFraction)
    $g.DrawLine($gridPen, $x, $plotTop - 20, $x, $plotTop + ($rows.Count * ($barHeight + $rowGap)) - 8)
    $label = "{0:P0}" -f $tick
    Draw-Text $g $label $fontSmall $muted ($x - 14) ($plotTop - 42)
}
$g.DrawLine($axisPen, $plotLeft, $plotTop - 15, $plotLeft, $plotTop + ($rows.Count * ($barHeight + $rowGap)) - 8)

$palette = @(
    [System.Drawing.Color]::FromArgb(39, 104, 115),
    [System.Drawing.Color]::FromArgb(62, 112, 72),
    [System.Drawing.Color]::FromArgb(73, 105, 150),
    [System.Drawing.Color]::FromArgb(111, 92, 158),
    [System.Drawing.Color]::FromArgb(180, 105, 50),
    [System.Drawing.Color]::FromArgb(158, 72, 55),
    [System.Drawing.Color]::FromArgb(115, 115, 115)
)

for ($i = 0; $i -lt $rows.Count; $i++) {
    $row = $rows[$i]
    $y = $plotTop + $i * ($barHeight + $rowGap)
    $fraction = [double]$row.creditable_fraction_of_gross
    $barWidth = [int]($plotWidth * $fraction / $maxFraction)
    $barBrush = [System.Drawing.SolidBrush]::new($palette[$i % $palette.Count])
    $g.FillRectangle($barBrush, $plotLeft, $y, $barWidth, $barHeight)
    $barBrush.Dispose()

    $shortName = $row.display_name
    if ($shortName.Length -gt 42) {
        $shortName = $shortName.Substring(0, 39) + "..."
    }
    Draw-Text $g $shortName $fontLabel $black $leftLabel ($y - 3)
    Draw-Text $g $row.risk_class $fontSmall $muted $leftLabel ($y + 22)

    $pct = "{0:P1}" -f $fraction
    $value = "$pct; $($row.creditable_gtco2_y_after_mrv) Gt/y; $($row.gross_to_creditable_multiplier)x gross/credit"
    Draw-Text $g $value $fontValue $black ($plotLeft + $barWidth + 14) ($y + 8)
}

$summaryY = 750
$summaryBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(238, 238, 230))
$g.FillRectangle($summaryBrush, 64, $summaryY, 1640, 100)
$summaryBrush.Dispose()
Draw-Text $g "Portfolio result" $fontLabel $black 88 ($summaryY + 18)
Draw-Text $g "100 GtCO2/y gross -> $($summary["lifecycle_durable_credit"]) GtCO2/y lifecycle-durable -> $($summary["mrv_creditable_total"]) GtCO2/y creditable after MRV and integrity buffers." $fontSubtitle $black 88 ($summaryY + 45)
Draw-Text $g "Same pathway mix needs $($summary["gross_required_for_100_credit_same_mix"]) GtCO2/y gross to credit 100 GtCO2/y, adding about $($summary["additional_gross_required_vs_100"]) GtCO2/y gross removal." $fontSubtitle $black 88 ($summaryY + 70)

Draw-Text $g "Stress-test anchors: EPA Class VI/Subpart RR, EU CRCF, Oxford durable-offsetting principles, State of CDR, and NASEM ocean CDR research gaps. Buffers are provisional." $fontFooter $muted 66 878
Draw-Text $g "AETHER should reject cheap gross tonnes that cannot survive measurement, attribution, permanence, invalidation, and liability accounting." $fontFooter $muted 66 904

$output = Join-Path $FigureDir "mrv_credit_integrity_overbuild.png"
Save-Png $bmp $output
$g.Dispose()
$bmp.Dispose()

Write-Host "Wrote $output"

