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

function Draw-WrappedText($Graphics, [string]$Text, $Font, $Brush, [float]$X, [float]$Y, [float]$Width, [float]$LineHeight) {
    $words = $Text -split "\s+"
    $line = ""
    foreach ($word in $words) {
        $candidate = if ([string]::IsNullOrWhiteSpace($line)) { $word } else { $line + " " + $word }
        if ($Graphics.MeasureString($candidate, $Font).Width -le $Width) {
            $line = $candidate
        } else {
            if (-not [string]::IsNullOrWhiteSpace($line)) {
                $Graphics.DrawString($line, $Font, $Brush, $X, $Y)
                $Y += $LineHeight
            }
            $line = $word
        }
    }
    if (-not [string]::IsNullOrWhiteSpace($line)) {
        $Graphics.DrawString($line, $Font, $Brush, $X, $Y)
        $Y += $LineHeight
    }
    return $Y
}

function Get-BarBrush([string]$Class) {
    if ($Class -eq "legacy DAC chemistry warning") {
        return New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(155, 74, 54))
    }
    if ($Class -eq "AETHER media requirement") {
        return New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(42, 119, 122))
    }
    if ($Class -eq "critical mineral") {
        return New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(105, 91, 151))
    }
    if ($Class -eq "power-system material") {
        return New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(66, 99, 142))
    }
    return New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(91, 125, 88))
}

$allRows = @(Import-Csv (Join-Path $TableDir "aether_material_supply_chain_requirements.csv"))
$selectedIds = @(
    "legacy_naoh_high",
    "legacy_naoh_low",
    "advanced_media_2pct_daccs",
    "advanced_media_0_5pct_daccs",
    "power_system_copper_3gj_balanced",
    "power_system_steel_3gj_balanced",
    "all_air_contactor_steel_moderate",
    "daccs_contactor_steel_moderate",
    "co2_corridor_pipeline_steel"
)
$rows = @()
foreach ($id in $selectedIds) {
    $rows += @($allRows | Where-Object { $_.row_id -eq $id })[0]
}

$width = 1600
$height = 1020
$bmp = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::FromArgb(250, 250, 247))

$titleFont = New-Object System.Drawing.Font("Arial", 28, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 14)
$labelFont = New-Object System.Drawing.Font("Arial", 12)
$boldFont = New-Object System.Drawing.Font("Arial", 12, [System.Drawing.FontStyle]::Bold)
$smallFont = New-Object System.Drawing.Font("Arial", 10)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(85, 85, 82), 2)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(220, 220, 214), 1)

$g.DrawString("AETHER Material and Industrial Supply-Chain Pressure", $titleFont, [System.Drawing.Brushes]::Black, 58, 38)
$g.DrawString("Annual material demand as a share of current global production comparators. Log scale; high-makeup DAC chemistry is the warning case.", $subFont, [System.Drawing.Brushes]::DimGray, 62, 84)

$left = 480
$top = 150
$barHeight = 34
$gap = 40
$plotWidth = 900
$minLog = -1.0
$maxLog = 3.0

function Map-X([double]$Pct) {
    $log = [math]::Log10([math]::Max($Pct, 0.1))
    return $left + (($log - $minLog) / ($maxLog - $minLog)) * $plotWidth
}

$ticks = @(0.1, 1, 10, 100, 1000)
foreach ($tick in $ticks) {
    $x = Map-X $tick
    $g.DrawLine($gridPen, $x, $top - 28, $x, $top + ($barHeight + $gap) * $rows.Count - $gap + 18)
    $tickLabel = if ($tick -lt 1) { "0.1%" } else { ([int]$tick).ToString() + "%" }
    $g.DrawString($tickLabel, $smallFont, [System.Drawing.Brushes]::DimGray, $x - 18, $top - 50)
}
$g.DrawLine($axisPen, (Map-X 0.1), $top - 22, (Map-X 0.1), $top + ($barHeight + $gap) * $rows.Count - $gap + 18)

for ($i = 0; $i -lt $rows.Count; $i++) {
    $row = $rows[$i]
    $y = $top + $i * ($barHeight + $gap)
    $pct = [double]$row.share_of_global_comparator_pct
    $x0 = Map-X 0.1
    $x1 = Map-X $pct
    $brush = Get-BarBrush $row.pressure_class
    $g.DrawString($row.figure_label, $boldFont, [System.Drawing.Brushes]::Black, 62, $y + 2)
    $g.DrawString($row.material_or_system, $smallFont, [System.Drawing.Brushes]::DimGray, 62, $y + 23)
    $g.FillRectangle($brush, [float]$x0, [float]$y, [float]([math]::Max(2, $x1 - $x0)), $barHeight)
    $valueText = ([double]$row.annualized_or_annual_material_mt_y).ToString("N0") + " Mt/y; " + $pct.ToString("0.#") + "%"
    $g.DrawString($valueText, $labelFont, [System.Drawing.Brushes]::Black, [float]([math]::Min($x1 + 12, 1375)), $y + 8)
}

$noteY = 835
$note = "Read this as a bottleneck screen, not a bill of materials. Structural steel and cement look large but potentially buildable under optimized designs. High-makeup reactive media is disqualifying. Copper, transformers, grid equipment, and chemical replacement loops become parallel constraints with clean-energy buildout."
$finalY = Draw-WrappedText $g $note $labelFont ([System.Drawing.Brushes]::Black) 64 $noteY 1410 20
$g.DrawString("Sources: World Steel Association 2025; USGS MCS 2025 cement chapter; IEA Critical Minerals Outlook 2025; WRI DAC impacts report; Chatterjee and Huang 2020. Several intensities are AETHER scenario assumptions.", $smallFont, [System.Drawing.Brushes]::DimGray, 64, ($finalY + 18))

$out = Join-Path $FigureDir "material_supply_chain_pressure.png"
Save-Png $bmp $out
$g.Dispose()
$bmp.Dispose()
Write-Host "Wrote $out"

