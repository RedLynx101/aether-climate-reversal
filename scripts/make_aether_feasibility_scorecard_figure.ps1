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

function Get-BrushForStatus {
    param([Parameter(Mandatory = $true)][string]$Status)
    $color = switch ($Status) {
        "conditional_pass" { [System.Drawing.Color]::FromArgb(76, 145, 96) }
        "upper_tail_dependency" { [System.Drawing.Color]::FromArgb(103, 126, 166) }
        "major_bottleneck" { [System.Drawing.Color]::FromArgb(191, 125, 55) }
        "research_gap" { [System.Drawing.Color]::FromArgb(132, 101, 158) }
        "governance_constraint" { [System.Drawing.Color]::FromArgb(166, 82, 75) }
        default { [System.Drawing.Color]::DimGray }
    }
    return New-Object System.Drawing.SolidBrush($color)
}

function Format-StatusLabel {
    param([Parameter(Mandatory = $true)][string]$Status)
    return ($Status -replace "_", " ").ToUpperInvariant()
}

$rows = @(Import-Csv (Join-Path $TableDir "aether_feasibility_gate_scorecard.csv") | Sort-Object {[int]$_.gate_order})

$width = 1800
$height = 1320
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font("Arial", 26, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 14)
$gateFont = New-Object System.Drawing.Font("Arial", 11, [System.Drawing.FontStyle]::Bold)
$labelFont = New-Object System.Drawing.Font("Arial", 9)
$statusFont = New-Object System.Drawing.Font("Arial", 8, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Consolas", 9)
$linePen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)

$g.DrawString("AETHER Feasibility Gate Scorecard", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("The 100 GtCO2/year case survives only if several physical, economic, governance, and evidence gates clear together.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$startY = 145
$rowH = 92
$gateX = 76
$statusX = 430
$anchorX = 690
$readX = 1180

$g.DrawString("Gate", $gateFont, [System.Drawing.Brushes]::Black, $gateX, 122)
$g.DrawString("Status", $gateFont, [System.Drawing.Brushes]::Black, $statusX, 122)
$g.DrawString("Quantitative anchor", $gateFont, [System.Drawing.Brushes]::Black, $anchorX, 122)
$g.DrawString("Current read", $gateFont, [System.Drawing.Brushes]::Black, $readX, 122)

for ($i = 0; $i -lt $rows.Count; $i++) {
    $row = $rows[$i]
    $y = $startY + $i * $rowH
    if ($i -gt 0) {
        $g.DrawLine($linePen, 66, $y - 12, $width - 70, $y - 12)
    }

    $statusBrush = Get-BrushForStatus $row.status
    $g.DrawString(("{0}. {1}" -f $row.gate_order, $row.gate), $gateFont, [System.Drawing.Brushes]::Black, $gateX, $y)
    $g.FillRectangle($statusBrush, $statusX, $y - 3, 205, 28)
    $g.DrawString((Format-StatusLabel $row.status), $statusFont, [System.Drawing.Brushes]::White, $statusX + 10, $y + 4)
    $anchorRect = New-Object System.Drawing.RectangleF([float]$anchorX, [float]$y, [float]455, [float]70)
    $readRect = New-Object System.Drawing.RectangleF([float]$readX, [float]$y, [float]540, [float]70)
    $g.DrawString($row.quantitative_anchor, $labelFont, [System.Drawing.Brushes]::DimGray, $anchorRect)
    $g.DrawString($row.current_read, $labelFont, [System.Drawing.Brushes]::DimGray, $readRect)
    $statusBrush.Dispose()
}

$g.DrawString("Interpretation: AETHER is not ruled out by first-order physics, but the current evidence supports a conditional research program rather than a central forecast.", $labelFont, [System.Drawing.Brushes]::DimGray, 66, $height - 84)
$g.DrawString("Source: aether_feasibility_gate_scorecard.csv, synthesized from the generated AETHER model suite.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 42)

Save-Png $bmp (Join-Path $FigureDir "feasibility_gate_scorecard.png")
$titleFont.Dispose(); $subFont.Dispose(); $gateFont.Dispose(); $labelFont.Dispose(); $statusFont.Dispose(); $footerFont.Dispose(); $linePen.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "feasibility_gate_scorecard.png") | Select-Object FullName,Length
