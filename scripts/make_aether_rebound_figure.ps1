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

$rows = Import-Csv (Join-Path $TableDir "aether_jevons_rebound_sensitivity.csv")
$w = 1400; $h = 900
$bmp = New-Object System.Drawing.Bitmap $w, $h
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(250,250,248))
$titleFont = New-Object System.Drawing.Font("Arial", 30, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 16)
$labelFont = New-Object System.Drawing.Font("Arial", 15)
$valueFont = New-Object System.Drawing.Font("Arial", 14, [System.Drawing.FontStyle]::Bold)
$smallFont = New-Object System.Drawing.Font("Arial", 12)
$g.DrawString("Jevons and Policy Rebound Sensitivity", $titleFont, [System.Drawing.Brushes]::Black, 70, 42)
$g.DrawString("100 GtCO2/year gross removal breaks even if rebound or delayed abatement reaches 57.8%.", $subFont, [System.Drawing.Brushes]::DimGray, 72, 88)
$left = 120; $right = 1260; $top = 155; $barH = 54; $gap = 31
$min = -45.0; $max = 60.0
$zeroX = $left + ((0 - $min) / ($max - $min)) * ($right - $left)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(224,224,220), 1)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(90,90,90), 3)
foreach ($tick in @(-40,-20,0,20,40,60)) {
    $x = $left + (($tick - $min) / ($max - $min)) * ($right - $left)
    $g.DrawLine($gridPen, [float]$x, $top - 20, [float]$x, $top + ($barH+$gap)*$rows.Count - $gap + 10)
    $g.DrawString(($tick.ToString() + " Gt"), $smallFont, [System.Drawing.Brushes]::DimGray, [float]($x - 24), 806)
}
$g.DrawLine($axisPen, [float]$zeroX, $top - 25, [float]$zeroX, $top + ($barH+$gap)*$rows.Count - $gap + 18)
$posBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(42,104,130))
$negBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(154,68,55))
for ($i=0; $i -lt $rows.Count; $i++) {
    $r = $rows[$i]
    $rebound = [double]$r.jevons_or_policy_rebound_fraction_of_gross_removal
    $net = [double]$r.net_removal_gtco2_y
    $y = $top + $i * ($barH + $gap)
    $g.DrawString($rebound.ToString("P0"), $labelFont, [System.Drawing.Brushes]::Black, 70, $y + 14)
    $x = $left + (($net - $min) / ($max - $min)) * ($right - $left)
    if ($net -ge 0) {
        $g.FillRectangle($posBrush, [float]$zeroX, $y, [float]($x - $zeroX), $barH)
        $g.DrawString($net.ToString("0.0") + " Gt net", $valueFont, [System.Drawing.Brushes]::Black, [float]($x + 14), $y + 14)
    } else {
        $g.FillRectangle($negBrush, [float]$x, $y, [float]($zeroX - $x), $barH)
        $g.DrawString($net.ToString("0.0") + " Gt net", $valueFont, [System.Drawing.Brushes]::White, [float]($x + 12), $y + 14)
    }
}
$g.DrawString("net annual CO2 removal after current emissions and rebound", $smallFont, [System.Drawing.Brushes]::DimGray, 520, 835)
$g.DrawString("Source: aether_transition_model.py, generated 2026-06-09.", $smallFont, [System.Drawing.Brushes]::DimGray, 70, 855)
Save-Png $bmp (Join-Path $FigureDir "jevons_rebound_sensitivity_100gt.png")
$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $valueFont.Dispose(); $smallFont.Dispose(); $gridPen.Dispose(); $axisPen.Dispose(); $posBrush.Dispose(); $negBrush.Dispose(); $g.Dispose(); $bmp.Dispose()
Get-Item (Join-Path $FigureDir "jevons_rebound_sensitivity_100gt.png") | Select-Object FullName,Length

