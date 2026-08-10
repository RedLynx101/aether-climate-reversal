$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$TableDir = Join-Path $Root "analysis\tables"
$FigureDir = Join-Path $Root "analysis\figures"
New-Item -ItemType Directory -Force -Path $FigureDir | Out-Null

function Save-Png {
    param(
        [Parameter(Mandatory = $true)][System.Drawing.Bitmap]$Bitmap,
        [Parameter(Mandatory = $true)][string]$Path
    )
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Force
    }
    $Bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
}

function Get-SummaryMap {
    $map = @{}
    Import-Csv (Join-Path $TableDir "aether_uncertainty_summary.csv") | ForEach-Object {
        $map[$_.metric] = [double]$_.value
    }
    return $map
}

$summary = Get-SummaryMap

$width = 1480
$height = 900
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font("Arial", 26, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 14)
$labelFont = New-Object System.Drawing.Font("Arial", 12)
$boldFont = New-Object System.Drawing.Font("Arial", 12, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Consolas", 9)
$barBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(56, 110, 132))
$accentBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(91, 143, 107))
$warningBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(202, 139, 64))
$weakBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(150, 81, 71))
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)

$g.DrawString("AETHER Monte Carlo Success Screen", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("20,000 draws across energy, clean power, robot supply, storage, budget, lifecycle durability, emissions, and rebound.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$items = @(
    @{ label = "Gross capacity >= 100 Gt/y"; metric = "gross_100_probability"; brush = $barBrush },
    @{ label = "Durable credit >= 100 Gt/y"; metric = "durable_100_probability"; brush = $accentBrush },
    @{ label = "Net after emissions/rebound > 0"; metric = "positive_climate_reversal_probability"; brush = $warningBrush },
    @{ label = "Net >= current annual emissions"; metric = "strong_reversal_probability"; brush = $weakBrush }
)

$left = 390
$top = 185
$maxW = 760
$barH = 46
$gap = 68
for ($tick = 0; $tick -le 100; $tick += 20) {
    $x = $left + ($maxW * $tick / 100)
    $g.DrawLine($gridPen, [float]$x, $top - 28, [float]$x, $top + ($barH + $gap) * $items.Count - 25)
    $g.DrawString("$tick%", $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 16), $top + ($barH + $gap) * $items.Count - 15)
}

for ($i = 0; $i -lt $items.Count; $i++) {
    $item = $items[$i]
    $value = [double]$summary[$item.metric]
    $y = $top + $i * ($barH + $gap)
    $g.DrawString($item.label, $boldFont, [System.Drawing.Brushes]::Black, 66, $y + 10)
    $w = $maxW * $value
    $g.FillRectangle($item.brush, $left, $y, [float]$w, $barH)
    $g.DrawString($value.ToString("0.0%"), $boldFont, [System.Drawing.Brushes]::Black, [float]($left + $w + 16), $y + 11)
}

$summaryText = "Median durable credit: " + $summary["durable_credit_p50"].ToString("0.0") + " Gt/y; P10-P90: " + $summary["durable_credit_p10"].ToString("0.0") + "-" + $summary["durable_credit_p90"].ToString("0.0") + " Gt/y. Median net after emissions/rebound: " + $summary["net_after_emissions_rebound_p50"].ToString("0.0") + " Gt/y."
$g.DrawString($summaryText, $labelFont, [System.Drawing.Brushes]::DimGray, 66, 680)
$g.DrawString("Source: aether_uncertainty_sensitivity_model.py; distributions are explicit AETHER assumptions, not forecasts.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 45)

Save-Png $bmp (Join-Path $FigureDir "uncertainty_success_probabilities.png")
$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$barBrush.Dispose(); $accentBrush.Dispose(); $warningBrush.Dispose(); $weakBrush.Dispose(); $gridPen.Dispose(); $g.Dispose(); $bmp.Dispose()

$rows = @(Import-Csv (Join-Path $TableDir "aether_uncertainty_sensitivity.csv") | Sort-Object { [Math]::Abs([double]$_.correlation_with_net_climate) } -Descending | Select-Object -First 10)
$width = 1480
$height = 960
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font("Arial", 26, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 14)
$labelFont = New-Object System.Drawing.Font("Arial", 11)
$boldFont = New-Object System.Drawing.Font("Arial", 11, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Consolas", 9)
$posBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(70, 135, 96))
$negBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(170, 89, 82))
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::DimGray, 2)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)

$g.DrawString("AETHER Sensitivity: What Controls Net Climate Result?", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("Pearson screen against 2046 net removal after lifecycle durability, residual emissions, and rebound.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$leftLabel = 66
$centerX = 690
$barMax = 520
$top = 150
$rowH = 64

for ($tick = -0.6; $tick -le 0.6; $tick += 0.2) {
    $x = $centerX + ($barMax * $tick / 0.6)
    $g.DrawLine($gridPen, [float]$x, $top - 20, [float]$x, $top + $rowH * $rows.Count + 8)
    $g.DrawString($tick.ToString("0.0"), $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 16), $top + $rowH * $rows.Count + 15)
}
$g.DrawLine($axisPen, $centerX, $top - 25, $centerX, $top + $rowH * $rows.Count + 5)

for ($i = 0; $i -lt $rows.Count; $i++) {
    $r = $rows[$i]
    $corr = [double]$r.correlation_with_net_climate
    $y = $top + $i * $rowH
    $label = $r.label
    if ($label.Length -gt 38) { $label = $label.Substring(0, 35) + "..." }
    $g.DrawString($label, $boldFont, [System.Drawing.Brushes]::Black, $leftLabel, $y + 14)
    $w = [Math]::Min($barMax, [Math]::Abs($corr) * $barMax / 0.6)
    if ($corr -ge 0) {
        $g.FillRectangle($posBrush, $centerX, $y + 13, [float]$w, 24)
        $g.DrawString($corr.ToString("0.00"), $labelFont, [System.Drawing.Brushes]::Black, [float]($centerX + $w + 10), $y + 13)
    } else {
        $g.FillRectangle($negBrush, [float]($centerX - $w), $y + 13, [float]$w, 24)
        if ($w -gt 80) {
            $g.DrawString($corr.ToString("0.00"), $labelFont, [System.Drawing.Brushes]::White, [float]($centerX - $w + 12), $y + 13)
        } else {
            $g.DrawString($corr.ToString("0.00"), $labelFont, [System.Drawing.Brushes]::Black, [float]($centerX - $w - 52), $y + 13)
        }
    }
}

$g.DrawString("Negative values reduce net climate benefit; positive values increase it. This is a first-order screen, not causal proof.", $labelFont, [System.Drawing.Brushes]::DimGray, 66, 835)
$g.DrawString("Source: aether_uncertainty_sensitivity_model.py; use for model triage before a publication-grade uncertainty analysis.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 45)

Save-Png $bmp (Join-Path $FigureDir "uncertainty_sensitivity_tornado.png")
$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$posBrush.Dispose(); $negBrush.Dispose(); $axisPen.Dispose(); $gridPen.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "uncertainty_success_probabilities.png"), (Join-Path $FigureDir "uncertainty_sensitivity_tornado.png") | Select-Object FullName,Length

