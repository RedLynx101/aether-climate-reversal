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

$scenarios = @(Import-Csv (Join-Path $TableDir "aether_cost_stack_scenarios.csv"))
$components = @(Import-Csv (Join-Path $TableDir "aether_cost_stack_components.csv"))

$componentOrder = @(
    "energy",
    "contactor_capex",
    "sorbent_materials",
    "compression_transport_storage",
    "mrv_insurance_liability",
    "robot_ops_maintenance",
    "finance_permitting_overhead",
    "product_handling"
)
$componentColors = @{
    "energy" = [System.Drawing.Color]::FromArgb(56, 110, 132)
    "contactor_capex" = [System.Drawing.Color]::FromArgb(202, 139, 64)
    "sorbent_materials" = [System.Drawing.Color]::FromArgb(129, 141, 76)
    "compression_transport_storage" = [System.Drawing.Color]::FromArgb(91, 143, 107)
    "mrv_insurance_liability" = [System.Drawing.Color]::FromArgb(118, 104, 154)
    "robot_ops_maintenance" = [System.Drawing.Color]::FromArgb(79, 132, 178)
    "finance_permitting_overhead" = [System.Drawing.Color]::FromArgb(148, 91, 82)
    "product_handling" = [System.Drawing.Color]::FromArgb(130, 130, 130)
}

$width = 1600
$height = 980
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font("Arial", 26, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 14)
$labelFont = New-Object System.Drawing.Font("Arial", 11)
$boldFont = New-Object System.Drawing.Font("Arial", 11, [System.Drawing.FontStyle]::Bold)
$footerFont = New-Object System.Drawing.Font("Consolas", 9)
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)

$g.DrawString("AETHER Delivered Cost Stack by Scenario", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("Energy floors separated from capex, materials, storage, MRV, robot operations, finance, and carbon/O2 handling.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 330
$top = 150
$maxW = 880
$barH = 42
$gap = 76
$maxCost = 650.0

for ($tick = 0; $tick -le 650; $tick += 100) {
    $x = $left + $maxW * $tick / $maxCost
    $g.DrawLine($gridPen, [float]$x, $top - 25, [float]$x, $top + ($barH + $gap) * $scenarios.Count - 20)
    $g.DrawString("$" + $tick.ToString(), $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 15), $top + ($barH + $gap) * $scenarios.Count - 8)
}

for ($i = 0; $i -lt $scenarios.Count; $i++) {
    $s = $scenarios[$i]
    $y = $top + $i * ($barH + $gap)
    $g.DrawString($s.display_name, $boldFont, [System.Drawing.Brushes]::Black, 66, $y + 9)
    $xCursor = [double]$left
    foreach ($component in $componentOrder) {
        $row = $components | Where-Object { $_.scenario -eq $s.scenario -and $_.component -eq $component } | Select-Object -First 1
        $cost = [double]$row.cost_usd_tco2
        if ($cost -le 0) { continue }
        $w = $maxW * $cost / $maxCost
        $brush = New-Object System.Drawing.SolidBrush($componentColors[$component])
        $g.FillRectangle($brush, [float]$xCursor, $y, [float]$w, $barH)
        $brush.Dispose()
        $xCursor += $w
    }
    $total = [double]$s.total_cost_usd_tco2
    $annual = [double]$s.annual_cost_at_100gt_trillion_usd_y
    $g.DrawString("$" + $total.ToString("0") + "/t; $" + $annual.ToString("0.0") + "T/y at 100 Gt", $boldFont, [System.Drawing.Brushes]::Black, [float]($xCursor + 12), $y + 9)
}

$legendX = 66
$legendY = 780
$legendItems = @(
    @("energy", "Energy"),
    @("contactor_capex", "Plant/contactors"),
    @("sorbent_materials", "Sorbents/materials"),
    @("compression_transport_storage", "Compression/storage"),
    @("mrv_insurance_liability", "MRV/liability"),
    @("robot_ops_maintenance", "Robot O&M"),
    @("finance_permitting_overhead", "Finance/permitting"),
    @("product_handling", "Carbon/O2 handling")
)
for ($i = 0; $i -lt $legendItems.Count; $i++) {
    $item = $legendItems[$i]
    $x = $legendX + ($i % 4) * 330
    $y = $legendY + [Math]::Floor($i / 4) * 34
    $brush = New-Object System.Drawing.SolidBrush($componentColors[$item[0]])
    $g.FillRectangle($brush, $x, $y, 24, 14)
    $brush.Dispose()
    $g.DrawString($item[1], $labelFont, [System.Drawing.Brushes]::Black, $x + 32, $y - 4)
}
$g.DrawString("Source: aether_cost_stack_model.py; scenario costs are explicit AETHER assumptions for feasibility-boundary analysis.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 45)

Save-Png $bmp (Join-Path $FigureDir "cost_stack_by_scenario.png")
$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$gridPen.Dispose(); $g.Dispose(); $bmp.Dispose()

$robots = @(Import-Csv (Join-Path $TableDir "aether_robot_labor_costs.csv"))
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
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)
$barBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(70, 135, 96))

$g.DrawString("Robot Hour Cost Is Not the Main AETHER Cost Floor", $titleFont, [System.Drawing.Brushes]::Black, 64, 42)
$g.DrawString("Unit-cost scenarios show why robotics can matter without pretending to beat energy, storage, and MRV floors.", $subFont, [System.Drawing.Brushes]::DimGray, 66, 88)

$left = 390
$top = 165
$maxW = 720
$barH = 48
$gap = 78
$maxCost = 24.0
for ($tick = 0; $tick -le 24; $tick += 4) {
    $x = $left + $maxW * $tick / $maxCost
    $g.DrawLine($gridPen, [float]$x, $top - 25, [float]$x, $top + ($barH + $gap) * $robots.Count - 25)
    $g.DrawString("$" + $tick.ToString(), $labelFont, [System.Drawing.Brushes]::DimGray, [float]($x - 12), $top + ($barH + $gap) * $robots.Count - 10)
}

for ($i = 0; $i -lt $robots.Count; $i++) {
    $r = $robots[$i]
    $y = $top + $i * ($barH + $gap)
    $cost = [double]$r.direct_robot_hour_cost_usd_h
    $w = $maxW * $cost / $maxCost
    $g.DrawString($r.display_name, $boldFont, [System.Drawing.Brushes]::Black, 66, $y + 12)
    $g.FillRectangle($barBrush, $left, $y, [float]$w, $barH)
    $unit = [double]$r.unit_cost_usd
    $g.DrawString("$" + $cost.ToString("0.00") + "/h; unit $" + ($unit / 1000).ToString("0") + "k", $boldFont, [System.Drawing.Brushes]::Black, [float]($left + $w + 14), $y + 12)
}

$g.DrawString("Direct robot-hour cost can fall by an order of magnitude, but AETHER still needs plant capex, sorbents, clean power, storage, MRV, insurance, and finance to fall together.", $labelFont, [System.Drawing.Brushes]::DimGray, 66, 715)
$g.DrawString("Source: aether_cost_stack_model.py; robot cases are AETHER assumptions for sensitivity work, not vendor quotes.", $footerFont, [System.Drawing.Brushes]::DimGray, 66, $height - 45)

Save-Png $bmp (Join-Path $FigureDir "robot_hour_cost_scenarios.png")
$titleFont.Dispose(); $subFont.Dispose(); $labelFont.Dispose(); $boldFont.Dispose(); $footerFont.Dispose()
$gridPen.Dispose(); $barBrush.Dispose(); $g.Dispose(); $bmp.Dispose()

Get-Item (Join-Path $FigureDir "cost_stack_by_scenario.png"), (Join-Path $FigureDir "robot_hour_cost_scenarios.png") | Select-Object FullName,Length
