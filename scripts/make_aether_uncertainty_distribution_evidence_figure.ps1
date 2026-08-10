$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$TableDir = Join-Path $Root "analysis\tables"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null
$OutPath = Join-Path $FigureDir "uncertainty_distribution_evidence_gaps.png"

$registry = @(Import-Csv (Join-Path $TableDir "aether_uncertainty_distribution_registry.csv") | Sort-Object {[int]$_.upgrade_priority}, evidence_grade, parameter)
$priorities = @(Import-Csv (Join-Path $TableDir "aether_uncertainty_distribution_upgrade_priorities.csv"))

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

function Shorten([string]$Text, [int]$MaxChars) {
    if ($Text.Length -le $MaxChars) {
        return $Text
    }
    return $Text.Substring(0, [Math]::Max(0, $MaxChars - 3)) + "..."
}

function Draw-Text($Graphics, [string]$Text, [System.Drawing.Font]$Font, [System.Drawing.Brush]$Brush, [float]$X, [float]$Y) {
    $Graphics.DrawString($Text, $Font, $Brush, [System.Drawing.PointF]::new($X, $Y))
}

$width = 1900
$height = 1000
$bmp = [System.Drawing.Bitmap]::new($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(249, 249, 246))

$titleFont = [System.Drawing.Font]::new("Arial", 31, [System.Drawing.FontStyle]::Bold)
$subFont = [System.Drawing.Font]::new("Arial", 15)
$headerFont = [System.Drawing.Font]::new("Arial", 13, [System.Drawing.FontStyle]::Bold)
$bodyFont = [System.Drawing.Font]::new("Arial", 11)
$smallFont = [System.Drawing.Font]::new("Arial", 9)
$black = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(24, 24, 24))
$muted = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(82, 82, 82))
$linePen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(214, 214, 208), 1)
$lightPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(232, 232, 226), 1)

$gradeColors = @{
    "A" = [System.Drawing.Color]::FromArgb(61, 132, 90)
    "B" = [System.Drawing.Color]::FromArgb(72, 138, 166)
    "C" = [System.Drawing.Color]::FromArgb(204, 143, 59)
    "D" = [System.Drawing.Color]::FromArgb(176, 82, 72)
}

Draw-Text $g "AETHER Uncertainty Distribution Evidence Gaps" $titleFont $black 70 42
Draw-Text $g "Every Monte Carlo input is mapped to evidence grade, source keys, distribution status, correlation family, and next upgrade task." $subFont $muted 72 88

$gradeCounts = @{}
foreach ($grade in @("A", "B", "C", "D")) { $gradeCounts[$grade] = 0 }
foreach ($row in $registry) { $gradeCounts[$row.evidence_grade] = [int]$gradeCounts[$row.evidence_grade] + 1 }
$priorityCounts = @{}
foreach ($p in 1..4) { $priorityCounts[[string]$p] = 0 }
foreach ($row in $registry) { $priorityCounts[$row.upgrade_priority] = [int]$priorityCounts[$row.upgrade_priority] + 1 }
$maxGrade = [Math]::Max(1, (($gradeCounts.Values | Measure-Object -Maximum).Maximum))
$maxPriority = [Math]::Max(1, (($priorityCounts.Values | Measure-Object -Maximum).Maximum))

Draw-Text $g "Evidence Grade Count" $headerFont $black 80 165
$barX = 150
$barTop = 215
$barWMax = 360
foreach ($grade in @("A", "B", "C", "D")) {
    $y = $barTop + (([int][char]$grade[0] - [int][char]'A') * 48)
    $count = [int]$gradeCounts[$grade]
    $brush = [System.Drawing.SolidBrush]::new($gradeColors[$grade])
    Draw-Text $g $grade $headerFont $black 85 ($y + 2)
    $g.FillRectangle($brush, $barX, $y, [float]($barWMax * $count / $maxGrade), 26)
    Draw-Text $g ([string]$count) $bodyFont $black ($barX + $barWMax + 18) ($y + 3)
    $brush.Dispose()
}

Draw-Text $g "Upgrade Priority Count" $headerFont $black 80 430
foreach ($p in 1..4) {
    $y = 480 + (($p - 1) * 48)
    $count = [int]$priorityCounts[[string]$p]
    $brush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(66, 100, 132))
    Draw-Text $g ([string]$p) $headerFont $black 85 ($y + 2)
    $g.FillRectangle($brush, $barX, $y, [float]($barWMax * $count / $maxPriority), 26)
    Draw-Text $g ([string]$count) $bodyFont $black ($barX + $barWMax + 18) ($y + 3)
    $brush.Dispose()
}

$tableX = 620
$tableTop = 162
Draw-Text $g "Parameter" $headerFont $black $tableX $tableTop
Draw-Text $g "Grade" $headerFont $black ($tableX + 420) $tableTop
Draw-Text $g "Priority" $headerFont $black ($tableX + 520) $tableTop
Draw-Text $g "Status" $headerFont $black ($tableX + 640) $tableTop
Draw-Text $g "Correlation Family" $headerFont $black ($tableX + 920) $tableTop

$rowY = $tableTop + 42
$rowH = 44
for ($i = 0; $i -lt $registry.Count; $i++) {
    $row = $registry[$i]
    $y = $rowY + ($i * $rowH)
    $g.DrawLine($lightPen, $tableX, $y - 10, $width - 70, $y - 10)
    Draw-Text $g (Shorten $row.label 48) $bodyFont $black $tableX $y
    $gradeBrush = [System.Drawing.SolidBrush]::new($gradeColors[$row.evidence_grade])
    $g.FillRectangle($gradeBrush, $tableX + 430, $y - 2, 36, 24)
    Draw-Text $g $row.evidence_grade $headerFont ([System.Drawing.Brushes]::White) ($tableX + 442) ($y - 1)
    Draw-Text $g $row.upgrade_priority $headerFont $black ($tableX + 548) $y
    Draw-Text $g (Shorten $row.current_distribution_status 30) $bodyFont $muted ($tableX + 640) $y
    Draw-Text $g (Shorten $row.correlation_family 42) $bodyFont $muted ($tableX + 920) $y
    $gradeBrush.Dispose()
}
$g.DrawLine($linePen, $tableX, $rowY - 14, $width - 70, $rowY - 14)

$priorityText = ($priorities | ForEach-Object { $_.priority_band + ": " + $_.parameter_count }) -join " | "
Draw-Text $g $priorityText $smallFont $muted 70 ($height - 72)
Draw-Text $g "Interpretation: v0.26 makes uncertainty inputs auditable. It does not turn hand-set triangular ranges into calibrated probabilities." $smallFont $muted 70 ($height - 45)

Save-Png $bmp $OutPath

$titleFont.Dispose(); $subFont.Dispose(); $headerFont.Dispose(); $bodyFont.Dispose(); $smallFont.Dispose()
$black.Dispose(); $muted.Dispose(); $linePen.Dispose(); $lightPen.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item -LiteralPath $OutPath | Select-Object FullName, Length, LastWriteTime

