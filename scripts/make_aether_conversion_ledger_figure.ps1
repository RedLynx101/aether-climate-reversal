$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$TableDir = Join-Path $Root "analysis\tables"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null

function Save-Png {
    param([Parameter(Mandatory = $true)][System.Drawing.Bitmap]$Bitmap, [Parameter(Mandatory = $true)][string]$Path)
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Force
    }
    $Bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
}

$states = @(Import-Csv (Join-Path $TableDir "aether_conversion_state_ledger.csv"))
$splits = @(Import-Csv (Join-Path $TableDir "aether_splitting_fraction_sensitivity.csv"))

$width = 1700
$height = 1120
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font("Arial", 26, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 14)
$sectionFont = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
$labelFont = New-Object System.Drawing.Font("Arial", 10)
$boldFont = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Consolas", 9)

$g.DrawString("AETHER Conversion Ledger: Storage Volume vs Splitting Energy", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("At 100 GtCO2/year, storage state changes volume by orders of magnitude, but CO2 splitting creates a huge energy burden.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 520
$maxW = 900
$barH = 34
$gap = 54
$minLog = 0.8
$maxLog = 5.0
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)
$co2Brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(65, 125, 145))
$carbonBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(205, 117, 45))
$mineralBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(83, 139, 94))

function Short-Text {
    param([string]$Text, [int]$MaxLength = 68)
    if ([string]::IsNullOrWhiteSpace($Text)) {
        return ""
    }
    if ($Text.Length -le $MaxLength) {
        return $Text
    }
    return $Text.Substring(0, $MaxLength - 3) + "..."
}

$top = 165
$g.DrawString("Annual physical volume by storage/product state", $sectionFont, [System.Drawing.Brushes]::Black, 66, $top - 48)
for ($tickPow = 1; $tickPow -le 5; $tickPow++) {
    $x = $left + $maxW * ($tickPow - $minLog) / ($maxLog - $minLog)
    $g.DrawLine($gridPen, [float]$x, $top - 12, [float]$x, $top + ($barH + $gap) * $states.Count - $gap + 10)
    $g.DrawString(("10^{0}" -f $tickPow), $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 14), $top + ($barH + $gap) * $states.Count - 20)
}

for ($i = 0; $i -lt $states.Count; $i++) {
    $row = $states[$i]
    $y = $top + $i * ($barH + $gap)
    $volume = [double]$row.volume_km3_y
    $logValue = [Math]::Log10([Math]::Max(1.0, $volume))
    $w = [Math]::Max(3, $maxW * ($logValue - $minLog) / ($maxLog - $minLog))
    $stateName = [string]$row.storage_state
    $brush = if ($stateName -like "Solid carbon*" -or $stateName -like "Liquid O2*") {
        $carbonBrush
    } elseif ($stateName -like "*carbonate*") {
        $mineralBrush
    } else {
        $co2Brush
    }
    $g.DrawString($stateName, $boldFont, [System.Drawing.Brushes]::Black, 66, $y + 0)
    $g.DrawString((Short-Text $row.scale_comparator), $labelFont, [System.Drawing.Brushes]::DimGray, 66, $y + 22)
    $g.FillRectangle($brush, $left, $y, [float]$w, $barH)
    $g.DrawString((("{0:N2} km3/year" -f $volume)), $boldFont, [System.Drawing.Brushes]::Black, [float]($left + $w + 14), $y + 8)
}

$chartTop = 690
$g.DrawString("Energy and coproduct burden as split fraction rises", $sectionFont, [System.Drawing.Brushes]::Black, 66, $chartTop - 46)
$axisLeft = 145
$axisTop = $chartTop
$axisWidth = 1250
$axisHeight = 250
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gray, 1)
$linePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(190, 85, 40), 4)
$pointBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(190, 85, 40))
$g.DrawRectangle($axisPen, $axisLeft, $axisTop, $axisWidth, $axisHeight)

for ($i = 0; $i -le 4; $i++) {
    $y = $axisTop + $axisHeight - ($axisHeight * $i / 4)
    $g.DrawLine($gridPen, $axisLeft, [float]$y, $axisLeft + $axisWidth, [float]$y)
    $label = "{0:N0} TWh/y" -f ($i * 100000)
    $g.DrawString($label, $labelFont, [System.Drawing.Brushes]::DimGray, 60, [float]($y - 8))
}

$previousPoint = $null
foreach ($row in $splits) {
    $fraction = [double]$row.split_fraction
    $energy = [double]$row.annual_energy_twh_y
    $x = $axisLeft + $axisWidth * $fraction
    $y = $axisTop + $axisHeight - ($axisHeight * $energy / 400000.0)
    if ($previousPoint -ne $null) {
        $g.DrawLine($linePen, [float]$previousPoint.X, [float]$previousPoint.Y, [float]$x, [float]$y)
    }
    $g.FillEllipse($pointBrush, [float]($x - 5), [float]($y - 5), 10, 10)
    $g.DrawString(("{0:P0}" -f $fraction), $labelFont, [System.Drawing.Brushes]::Black, [float]($x - 14), $axisTop + $axisHeight + 10)
    if ($fraction -eq 0 -or $fraction -eq 0.25 -or $fraction -eq 1.0) {
        $g.DrawString(("{0:N0}" -f $energy), $boldFont, [System.Drawing.Brushes]::Black, [float]($x - 24), [float]($y - 24))
    }
    $previousPoint = [pscustomobject]@{ X = $x; Y = $y }
}

$g.DrawString("Split fraction of captured CO2", $labelFont, [System.Drawing.Brushes]::DimGray, $axisLeft + 470, $axisTop + $axisHeight + 42)
$g.DrawString("Includes 3 GJ/tCO2 capture plus 8.94 GJ/tCO2 times split fraction.", $labelFont, [System.Drawing.Brushes]::DimGray, $axisLeft, $axisTop + $axisHeight + 70)
$g.DrawString("Horizontal volume scale is log10. Orange is full-splitting product/coproduct; green is mineral-carbonate proxy.", $labelFont, [System.Drawing.Brushes]::DimGray, 66, 1034)
$g.DrawString("Source: aether_conversion_state_ledger.csv and aether_splitting_fraction_sensitivity.csv.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 42)

Save-Png $bmp (Join-Path $FigureDir "conversion_storage_ledger_100gt.png")
$titleFont.Dispose(); $subFont.Dispose(); $sectionFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$gridPen.Dispose(); $axisPen.Dispose(); $linePen.Dispose(); $co2Brush.Dispose(); $carbonBrush.Dispose(); $mineralBrush.Dispose(); $pointBrush.Dispose()
$g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "conversion_storage_ledger_100gt.png") | Select-Object FullName,Length
