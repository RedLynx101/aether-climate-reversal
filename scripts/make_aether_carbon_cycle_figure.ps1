$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$Table = Join-Path $Root "analysis\tables\aether_carbon_cycle_pathways.csv"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null
$OutPath = Join-Path $FigureDir "carbon_cycle_atmospheric_co2_pathways.png"

function Save-Png($Bitmap, [string]$Path) {
    $ms = New-Object System.IO.MemoryStream
    $Bitmap.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
    [System.IO.File]::WriteAllBytes($Path, $ms.ToArray())
    $ms.Dispose()
}

$rows = Import-Csv $Table
$cases = @(
    "baseline_constant_emissions_no_aether",
    "aether_constant_emissions_no_rebound",
    "aether_constant_emissions_58pct_rebound",
    "aether_half_2046_zero_2060",
    "aether_net_zero_2050",
    "aether_net_zero_2050_25pct_rebound"
)
$colors = @{
    "baseline_constant_emissions_no_aether" = [System.Drawing.Color]::FromArgb(90, 90, 90)
    "aether_constant_emissions_no_rebound" = [System.Drawing.Color]::FromArgb(40, 105, 150)
    "aether_constant_emissions_58pct_rebound" = [System.Drawing.Color]::FromArgb(190, 76, 60)
    "aether_half_2046_zero_2060" = [System.Drawing.Color]::FromArgb(88, 145, 90)
    "aether_net_zero_2050" = [System.Drawing.Color]::FromArgb(36, 125, 112)
    "aether_net_zero_2050_25pct_rebound" = [System.Drawing.Color]::FromArgb(205, 140, 48)
}

$width = 1500
$height = 950
$left = 105
$right = 435
$top = 145
$bottom = 130
$plotW = $width - $left - $right
$plotH = $height - $top - $bottom

$bmp = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(250,250,248))

$titleFont = New-Object System.Drawing.Font("Arial", 30, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 15)
$axisFont = New-Object System.Drawing.Font("Arial", 12)
$legendFont = New-Object System.Drawing.Font("Arial", 13)
$footerFont = New-Object System.Drawing.Font("Arial", 11)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(90,90,90), 2)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(225,225,220), 1)

$g.DrawString("AETHER Carbon-Cycle Pathways", $titleFont, [System.Drawing.Brushes]::Black, 70, 40)
$g.DrawString("Reduced-form Joos impulse response; managed AETHER scenarios throttle near 350 ppm.", $subFont, [System.Drawing.Brushes]::DimGray, 72, 86)

$allValues = @($rows | ForEach-Object { [double]$_.atmospheric_co2_ppm_reduced_form })
$minY = [Math]::Floor((($allValues | Measure-Object -Minimum).Minimum - 20) / 50) * 50
$maxY = [Math]::Ceiling((($allValues | Measure-Object -Maximum).Maximum + 20) / 50) * 50
$minYear = 2026
$maxYear = 2100

function XForYear([double]$Year) {
    return $left + (($Year - $minYear) / ($maxYear - $minYear)) * $plotW
}

function YForPpm([double]$Ppm) {
    return $top + (($maxY - $Ppm) / ($maxY - $minY)) * $plotH
}

for ($ppm = $minY; $ppm -le $maxY; $ppm += 50) {
    $y = YForPpm $ppm
    $g.DrawLine($gridPen, $left, $y, $left + $plotW, $y)
    $g.DrawString([string]$ppm, $axisFont, [System.Drawing.Brushes]::DimGray, 58, $y - 9)
}
foreach ($year in @(2030, 2040, 2050, 2060, 2080, 2100)) {
    $x = XForYear $year
    $g.DrawLine($gridPen, $x, $top, $x, $top + $plotH)
    $g.DrawString([string]$year, $axisFont, [System.Drawing.Brushes]::DimGray, $x - 16, $top + $plotH + 14)
}

$g.DrawLine($axisPen, $left, $top, $left, $top + $plotH)
$g.DrawLine($axisPen, $left, $top + $plotH, $left + $plotW, $top + $plotH)
$g.DrawString("ppm", $axisFont, [System.Drawing.Brushes]::DimGray, 54, $top - 30)
$g.DrawString("year", $axisFont, [System.Drawing.Brushes]::DimGray, $left + $plotW - 18, $top + $plotH + 45)

$legendX = $left + $plotW + 40
$legendY = $top + 8
foreach ($case in $cases) {
    $caseRows = @($rows | Where-Object { $_.case -eq $case } | Sort-Object {[int]$_.year})
    $pen = New-Object System.Drawing.Pen($colors[$case], 3.2)
    $points = New-Object System.Collections.Generic.List[System.Drawing.PointF]
    foreach ($r in $caseRows) {
        $points.Add([System.Drawing.PointF]::new((XForYear ([double]$r.year)), (YForPpm ([double]$r.atmospheric_co2_ppm_reduced_form))))
    }
    if ($points.Count -gt 1) {
        $g.DrawLines($pen, $points.ToArray())
    }
    $displayName = $caseRows[0].display_name
    $brush = New-Object System.Drawing.SolidBrush($colors[$case])
    $g.FillRectangle($brush, $legendX, $legendY + 5, 26, 5)
    $g.DrawString($displayName, $legendFont, [System.Drawing.Brushes]::Black, $legendX + 38, $legendY - 2)
    $final = $caseRows[-1]
    $g.DrawString(("2100: " + ([double]$final.atmospheric_co2_ppm_reduced_form).ToString("0") + " ppm"), $axisFont, [System.Drawing.Brushes]::DimGray, $legendX + 38, $legendY + 20)
    $legendY += 70
    $pen.Dispose()
    $brush.Dispose()
}

$g.DrawString("Source: aether_carbon_cycle_model.py. This is a reduced-form scenario comparison, not an Earth-system model.", $footerFont, [System.Drawing.Brushes]::DimGray, 70, $height - 48)
Save-Png $bmp $OutPath

$titleFont.Dispose(); $subFont.Dispose(); $axisFont.Dispose(); $legendFont.Dispose(); $footerFont.Dispose()
$axisPen.Dispose(); $gridPen.Dispose(); $g.Dispose(); $bmp.Dispose()
Get-Item $OutPath | Select-Object FullName,Length
