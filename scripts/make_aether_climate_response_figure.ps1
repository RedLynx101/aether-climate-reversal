$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$Table = Join-Path $Root "analysis\tables\aether_climate_response_pathways.csv"
$SummaryTable = Join-Path $Root "analysis\tables\aether_climate_response_summary.csv"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null
$OutPath = Join-Path $FigureDir "climate_response_temperature_proxy.png"

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
$summary = @(Import-Csv $SummaryTable)
$summaryByCase = @{}
$summary | ForEach-Object { $summaryByCase[$_.case] = $_ }

$cases = @(
    "baseline_constant_emissions_no_aether",
    "aether_constant_emissions_no_rebound",
    "aether_constant_emissions_58pct_rebound",
    "aether_half_2046_zero_2060",
    "aether_net_zero_2050",
    "aether_net_zero_2050_25pct_rebound"
)
$colors = @{
    "baseline_constant_emissions_no_aether" = [System.Drawing.Color]::FromArgb(70, 70, 70)
    "aether_constant_emissions_no_rebound" = [System.Drawing.Color]::FromArgb(38, 105, 142)
    "aether_constant_emissions_58pct_rebound" = [System.Drawing.Color]::FromArgb(184, 69, 54)
    "aether_half_2046_zero_2060" = [System.Drawing.Color]::FromArgb(84, 141, 88)
    "aether_net_zero_2050" = [System.Drawing.Color]::FromArgb(31, 122, 115)
    "aether_net_zero_2050_25pct_rebound" = [System.Drawing.Color]::FromArgb(207, 139, 44)
}

$width = 1740
$height = 1030
$left = 120
$right = 470
$top = 152
$bottom = 150
$plotW = $width - $left - $right
$plotH = $height - $top - $bottom

$bmp = [System.Drawing.Bitmap]::new($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(249, 249, 246))

$titleFont = [System.Drawing.Font]::new("Arial", 31, [System.Drawing.FontStyle]::Bold)
$subFont = [System.Drawing.Font]::new("Arial", 15)
$axisFont = [System.Drawing.Font]::new("Arial", 12)
$legendFont = [System.Drawing.Font]::new("Arial", 12)
$legendBoldFont = [System.Drawing.Font]::new("Arial", 12, [System.Drawing.FontStyle]::Bold)
$footerFont = [System.Drawing.Font]::new("Arial", 10)
$axisPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(85, 85, 85), 2)
$gridPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(222, 222, 216), 1)
$black = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(24, 24, 24))
$muted = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(82, 82, 82))

Draw-Text $g "AETHER Climate-Response Proxy" $titleFont $black 70 42
Draw-Text $g "CO2-only transient-scaled temperature proxy from AR6 forcing/sensitivity anchors; this is not a full Earth-system forecast." $subFont $muted 72 88

$allValues = @($rows | ForEach-Object { [double]$_.co2_only_transient_warming_proxy_c })
$minY = [Math]::Floor((($allValues | Measure-Object -Minimum).Minimum - 0.12) * 10) / 10
$maxY = [Math]::Ceiling((($allValues | Measure-Object -Maximum).Maximum + 0.12) * 10) / 10
$minYear = 2026
$maxYear = 2100

function XForYear([double]$Year) {
    return $left + (($Year - $minYear) / ($maxYear - $minYear)) * $plotW
}

function YForTemp([double]$Temp) {
    return $top + (($maxY - $Temp) / ($maxY - $minY)) * $plotH
}

for ($temp = $minY; $temp -le ($maxY + 0.001); $temp += 0.2) {
    $y = YForTemp $temp
    $g.DrawLine($gridPen, $left, $y, $left + $plotW, $y)
    Draw-Text $g ($temp.ToString("0.0")) $axisFont $muted 70 ($y - 9)
}
foreach ($year in @(2030, 2040, 2050, 2060, 2080, 2100)) {
    $x = XForYear $year
    $g.DrawLine($gridPen, $x, $top, $x, $top + $plotH)
    Draw-Text $g ([string]$year) $axisFont $muted ($x - 16) ($top + $plotH + 16)
}

$g.DrawLine($axisPen, $left, $top, $left, $top + $plotH)
$g.DrawLine($axisPen, $left, $top + $plotH, $left + $plotW, $top + $plotH)
Draw-Text $g "CO2-only proxy, deg C" $axisFont $muted 50 122
Draw-Text $g "year" $axisFont $muted ($left + $plotW - 18) ($top + $plotH + 48)

$legendX = $left + $plotW + 38
$legendY = $top + 4
foreach ($case in $cases) {
    $caseRows = @($rows | Where-Object { $_.case -eq $case } | Sort-Object {[int]$_.year})
    $pen = [System.Drawing.Pen]::new($colors[$case], 3.2)
    $points = [System.Collections.Generic.List[System.Drawing.PointF]]::new()
    foreach ($r in $caseRows) {
        $points.Add([System.Drawing.PointF]::new((XForYear ([double]$r.year)), (YForTemp ([double]$r.co2_only_transient_warming_proxy_c))))
    }
    if ($points.Count -gt 1) {
        $g.DrawLines($pen, $points.ToArray())
    }

    $brush = [System.Drawing.SolidBrush]::new($colors[$case])
    $g.FillRectangle($brush, $legendX, $legendY + 7, 26, 5)
    $displayName = $caseRows[0].display_name
    Draw-Text $g $displayName $legendBoldFont $black ($legendX + 38) ($legendY - 2)
    $final = $summaryByCase[$case]
    $detail = "2100: " + ([double]$final.co2_only_transient_proxy_2100_c).ToString("0.00") + " deg C; avoided vs no-AETHER: " + ([double]$final.transient_proxy_avoided_vs_no_aether_2100_c).ToString("0.00") + " deg C"
    Draw-Text $g $detail $legendFont $muted ($legendX + 38) ($legendY + 20)
    $legendY += 72
    $pen.Dispose()
    $brush.Dispose()
}

Draw-Text $g "Formula: FCO2 = 3.93 * log2(C/278); transient proxy = FCO2 / 3.93 * 1.8 deg C. Source anchors: IPCC AR6 WGI Ch. 7 and Technical Summary." $footerFont $muted 70 ($height - 66)
Draw-Text $g "Excludes non-CO2 forcing, aerosols, ocean heat uptake dynamics, ice sheets, regional response, and full carbon-climate feedbacks. Replace with FAIR/ESM before publication claims." $footerFont $muted 70 ($height - 42)

Save-Png $bmp $OutPath

$titleFont.Dispose(); $subFont.Dispose(); $axisFont.Dispose(); $legendFont.Dispose(); $legendBoldFont.Dispose(); $footerFont.Dispose()
$axisPen.Dispose(); $gridPen.Dispose(); $black.Dispose(); $muted.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item $OutPath | Select-Object FullName,Length

