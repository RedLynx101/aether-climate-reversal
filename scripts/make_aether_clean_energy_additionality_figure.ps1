$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$Table = Join-Path $Root "analysis\tables\aether_clean_energy_additionality_cases.csv"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null
$OutPath = Join-Path $FigureDir "clean_energy_additionality_gate.png"

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
$order = @(
    "status_quo_friction",
    "market_unlocked_texas_style",
    "aether_dedicated_buildout",
    "abundance_clean_power_push",
    "dirty_or_nonadditional_grid"
)
$labelMap = @{
    "status_quo_friction" = "Status quo friction"
    "market_unlocked_texas_style" = "Market unlocked"
    "aether_dedicated_buildout" = "Dedicated AETHER"
    "abundance_clean_power_push" = "Abundance push"
    "dirty_or_nonadditional_grid" = "Nonadditional grid"
}

$target = [double](@($rows | Where-Object { $_.scenario -eq "status_quo_friction" })[0].target_3gj_balanced_gross_generation_twh_y)
$maxX = 140000.0
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
$labelFont = [System.Drawing.Font]::new("Arial", 13)
$boldFont = [System.Drawing.Font]::new("Arial", 13, [System.Drawing.FontStyle]::Bold)
$footerFont = [System.Drawing.Font]::new("Arial", 10)
$black = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(24, 24, 24))
$muted = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(82, 82, 82))
$failBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(181, 82, 72))
$midBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(206, 153, 70))
$passBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(74, 134, 105))
$gridPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(224, 224, 218), 1)
$axisPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(85, 85, 85), 2)
$targetPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(36, 85, 120), 3)
$targetPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash

Draw-Text $g "AETHER Clean-Power Additionality Gate" $titleFont $black 64 42
Draw-Text $g "Total clean buildout is filtered by delivery, competing demand, and whether power is truly additional." $subFont $muted 66 88

$left = 360
$top = 180
$plotW = 900
$barH = 48
$rowGap = 92
$axisY = $top + $rowGap * $order.Count + 10

for ($tick = 0; $tick -le 140000; $tick += 20000) {
    $x = $left + $plotW * $tick / $maxX
    $g.DrawLine($gridPen, $x, $top - 18, $x, $axisY)
    Draw-Text $g (($tick / 1000).ToString("0") + "k") $axisFont $muted ($x - 10) ($axisY + 12)
}
$g.DrawLine($axisPen, $left, $axisY, $left + $plotW, $axisY)

$targetX = $left + $plotW * $target / $maxX
$g.DrawLine($targetPen, $targetX, $top - 30, $targetX, $axisY + 2)
Draw-Text $g "3 GJ/tCO2 gross target" $boldFont $black ($targetX - 86) ($top - 58)
Draw-Text $g "TWh/year of additional AETHER clean generation" $axisFont $muted $left ($axisY + 42)

for ($i = 0; $i -lt $order.Count; $i++) {
    $case = $order[$i]
    $row = @($rows | Where-Object { $_.scenario -eq $case })[0]
    $value = [double]$row.truly_additional_aether_clean_generation_twh_y
    $share = [double]$row.share_of_3gj_balanced_target
    $barW = [math]::Min($plotW * $value / $maxX, $plotW)
    $y = $top + $i * $rowGap
    $brush = if ($share -ge 1.0) { $passBrush } elseif ($share -ge 0.5) { $midBrush } else { $failBrush }
    Draw-Text $g $labelMap[$case] $boldFont $black 64 ($y + 8)
    Draw-Text $g ("additionality " + ([double]$row.additionality_fraction).ToString("0%")) $axisFont $muted 64 ($y + 34)
    $g.FillRectangle($brush, $left, $y, [float]$barW, $barH)
    Draw-Text $g (($value / 1000).ToString("0.0") + "k TWh/y") $labelFont $black ($left + $barW + 12) ($y + 4)
    Draw-Text $g (($share * 100).ToString("0") + "% of target") $axisFont $muted ($left + $barW + 12) ($y + 29)
}

$noteX = 1310
Draw-Text $g "Read:" $boldFont $black $noteX 245
Draw-Text $g "Cheap clean energy helps," $labelFont $muted $noteX 278
Draw-Text $g "but AETHER needs delivered," $labelFont $muted $noteX 302
Draw-Text $g "additional clean power." $labelFont $muted $noteX 326
Draw-Text $g "Market pull is useful;" $labelFont $muted $noteX 390
Draw-Text $g "nonadditional grid draw" $labelFont $muted $noteX 414
Draw-Text $g "fails the climate purpose." $labelFont $muted $noteX 438

Draw-Text $g "Source: aether_clean_energy_additionality_model.py. Scenario filters are explicit assumptions anchored to current clean-energy, grid, data-center, nuclear, and geothermal sources." $footerFont $muted 64 ($height - 48)

Save-Png $bmp $OutPath
$g.Dispose()
$bmp.Dispose()

Get-Item -LiteralPath $OutPath | Select-Object FullName, Length, LastWriteTime

