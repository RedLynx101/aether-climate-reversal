$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$TableDir = Join-Path $Root "analysis\tables"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null

function Save-Png {
    param([Parameter(Mandatory = $true)][System.Drawing.Bitmap]$Bitmap, [Parameter(Mandatory = $true)][string]$Path)
    if (Test-Path -LiteralPath $Path) { Remove-Item -LiteralPath $Path -Force }
    $Bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
}

$rows = @(Import-Csv (Join-Path $TableDir "aether_robotics_scale_comparison.csv"))
$annual = @($rows | Where-Object { $_.group -eq "Annual flow" })
$stock = @($rows | Where-Object { $_.group -eq "Stock or fleet" })

$width = 1600
$height = 1040
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font("Arial", 25, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 14)
$groupFont = New-Object System.Drawing.Font("Arial", 15, [System.Drawing.FontStyle]::Bold)
$labelFont = New-Object System.Drawing.Font("Arial", 10)
$boldFont = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Consolas", 9)

$g.DrawString("Robotics Scale Anchors vs AETHER Robot Needs", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("Company announcements show real acceleration, but AETHER requires industrial-scale useful work, not only cheap units.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 460
$maxW = 850
$barH = 30
$gap = 44
$minLog = 3.0
$maxLog = 8.1
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)
$annualBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(55, 111, 135))
$stockBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(83, 139, 94))
$aetherBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(205, 117, 45))

function Draw-Group {
    param($Rows, [string]$Title, [int]$Top, [System.Drawing.Brush]$DefaultBrush)
    $g.DrawString($Title, $groupFont, [System.Drawing.Brushes]::Black, 66, $Top - 38)
    for ($tickPow = 3; $tickPow -le 8; $tickPow++) {
        $x = $left + $maxW * ($tickPow - $minLog) / ($maxLog - $minLog)
        $g.DrawLine($gridPen, [float]$x, $Top - 8, [float]$x, $Top + ($barH + $gap) * $Rows.Count - $gap + 6)
        $tickLabel = "10^" + $tickPow
        $g.DrawString($tickLabel, $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 12), $Top + ($barH + $gap) * $Rows.Count - 20)
    }
    for ($i = 0; $i -lt $Rows.Count; $i++) {
        $row = $Rows[$i]
        $y = $Top + $i * ($barH + $gap)
        $value = [double]$row.value
        $logValue = [Math]::Log10($value)
        $w = [Math]::Max(3, $maxW * ($logValue - $minLog) / ($maxLog - $minLog))
        $brush = if ($row.label -like "AETHER*") { $aetherBrush } else { $DefaultBrush }
        $g.DrawString($row.label, $boldFont, [System.Drawing.Brushes]::Black, 66, $y + 2)
        $g.DrawString($row.interpretation, $labelFont, [System.Drawing.Brushes]::DimGray, 66, $y + 22)
        $g.FillRectangle($brush, $left, $y, [float]$w, $barH)
        $g.DrawString($value.ToString("N0") + " " + $row.unit, $boldFont, [System.Drawing.Brushes]::Black, [float]($left + $w + 14), $y + 5)
    }
}

Draw-Group $annual "Annual robot production / installation flow" 160 $annualBrush
Draw-Group $stock "Robot stock / fleet scale" 635 $stockBrush

$g.DrawString("Horizontal scale is log10. Orange bars are AETHER model requirements, not observed production.", $labelFont, [System.Drawing.Brushes]::DimGray, 66, 955)
$g.DrawString("Source: aether_robotics_scale_comparison.csv; IFR, Amazon, Unitree, Figure, and Agility source-register entries.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 45)

Save-Png $bmp (Join-Path $FigureDir "robotics_scale_anchors_vs_aether.png")
$titleFont.Dispose(); $subFont.Dispose(); $groupFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$gridPen.Dispose(); $annualBrush.Dispose(); $stockBrush.Dispose(); $aetherBrush.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "robotics_scale_anchors_vs_aether.png") | Select-Object FullName,Length
