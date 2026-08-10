$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot
$RequirementPath = Join-Path $Root "analysis\tables\aether_species_emissions_requirement_matrix.csv"
$GatePath = Join-Path $Root "analysis\tables\aether_species_emissions_publication_gates.csv"
$Output = Join-Path $Root "analysis\figures\species_emissions_handoff_gap_matrix.png"

$requirements = @(Import-Csv -LiteralPath $RequirementPath)
$gates = @(Import-Csv -LiteralPath $GatePath)

function Count-Where {
    param([array]$Rows, [scriptblock]$Predicate)
    return @($Rows | Where-Object $Predicate).Count
}

$statusRows = @(
    [pscustomobject]@{ Label = "usable screen"; Count = Count-Where $requirements { $_.current_status -eq "usable_screen" }; Color = [System.Drawing.Color]::FromArgb(20, 148, 136) },
    [pscustomobject]@{ Label = "provisional proxy"; Count = Count-Where $requirements { $_.current_status -eq "provisional_proxy" }; Color = [System.Drawing.Color]::FromArgb(37, 99, 235) },
    [pscustomobject]@{ Label = "aggregate placeholder"; Count = Count-Where $requirements { $_.current_status -eq "aggregate_placeholder" }; Color = [System.Drawing.Color]::FromArgb(217, 119, 6) },
    [pscustomobject]@{ Label = "missing"; Count = Count-Where $requirements { $_.current_status -eq "missing" }; Color = [System.Drawing.Color]::FromArgb(190, 64, 64) }
)

$width = 1600
$height = 980
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$g.Clear([System.Drawing.Color]::White)

$titleFont = New-Object System.Drawing.Font "Segoe UI", 28, ([System.Drawing.FontStyle]::Bold)
$subtitleFont = New-Object System.Drawing.Font "Segoe UI", 14, ([System.Drawing.FontStyle]::Regular)
$labelFont = New-Object System.Drawing.Font "Segoe UI", 12, ([System.Drawing.FontStyle]::Regular)
$labelBold = New-Object System.Drawing.Font "Segoe UI", 12, ([System.Drawing.FontStyle]::Bold)
$smallFont = New-Object System.Drawing.Font "Segoe UI", 10, ([System.Drawing.FontStyle]::Regular)

$ink = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(15, 23, 42))
$muted = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(71, 85, 105))
$gridPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(226, 232, 240)), 1

$g.DrawString("AETHER species-emissions FAIR handoff", $titleFont, $ink, 64, 42)
$g.DrawString("Publication gate for moving from aggregate forcing to species-level FAIR or Earth-system climate claims.", $subtitleFont, $muted, 66, 91)

$panelX = 80
$panelY = 155
$barMax = [Math]::Max(1, ($statusRows | ForEach-Object { $_.Count } | Measure-Object -Maximum).Maximum)
$barScale = 520.0 / $barMax
$g.DrawString("Current input status by species or forcing family", $labelBold, $ink, $panelX, $panelY)
$g.DrawString("These are model-input families, not physical emissions totals.", $smallFont, $muted, $panelX, $panelY + 28)

for ($i = 0; $i -lt $statusRows.Count; $i++) {
    $row = $statusRows[$i]
    $y = $panelY + 80 + ($i * 84)
    $barW = [float]($row.Count * $barScale)
    $brush = New-Object System.Drawing.SolidBrush $row.Color
    $g.DrawString($row.Label, $labelFont, $ink, $panelX, $y - 26)
    $g.FillRectangle($brush, $panelX, $y, $barW, 30)
    $g.DrawRectangle($gridPen, $panelX, $y, 520, 30)
    $g.DrawString([string]$row.Count, $labelBold, $ink, $panelX + 540, $y + 2)
}

$gateX = 830
$gateY = 155
$g.DrawString("Publication gates", $labelBold, $ink, $gateX, $gateY)
$g.DrawString("P0 gates must pass before temperature outputs become publication-grade.", $smallFont, $muted, $gateX, $gateY + 28)

for ($i = 0; $i -lt $gates.Count; $i++) {
    $row = $gates[$i]
    $y = $gateY + 78 + ($i * 62)
    $status = [string]$row.gate_status
    $color = if ($status -eq "partial") {
        [System.Drawing.Color]::FromArgb(217, 119, 6)
    } elseif ($status -eq "pass") {
        [System.Drawing.Color]::FromArgb(20, 148, 136)
    } else {
        [System.Drawing.Color]::FromArgb(190, 64, 64)
    }
    $brush = New-Object System.Drawing.SolidBrush $color
    $g.FillRectangle($brush, $gateX, $y, 16, 16)
    $g.DrawString("$($row.gate_id): $($row.gate_status) / $($row.priority)", $smallFont, $ink, $gateX + 28, $y - 4)
    $g.DrawString($row.test, $smallFont, $muted, (New-Object System.Drawing.RectangleF ($gateX + 28), ($y + 18), 610, 40))
}

$p0Blocking = Count-Where $requirements { $_.priority -eq "P0" -and $_.current_status -ne "usable_screen" }
$missing = Count-Where $requirements { $_.current_status -eq "missing" }
$aggregate = Count-Where $requirements { $_.current_status -eq "aggregate_placeholder" }
$score = (($requirements | ForEach-Object { [double]$_.readiness_score_0_1 } | Measure-Object -Average).Average).ToString("0.00", [System.Globalization.CultureInfo]::InvariantCulture)
$note = "Read: this layer is a handoff and blocker map. It preserves the FAIR package run but marks species-level CH4, N2O, aerosol precursors, land-use, lifecycle species traces, spin-up, ZEC, and uncertainty ensembles as unresolved."
$g.DrawString("Readiness score: $score   P0 blocking families: $p0Blocking   Missing: $missing   Aggregate placeholders: $aggregate", $labelBold, $ink, 64, 850)
$g.DrawString($note, $subtitleFont, $muted, (New-Object System.Drawing.RectangleF 64, 884, 1460, 48))
$g.DrawString("Source: aether_species_emissions_handoff_model.py using aether_fair_readiness_input_deck.csv.", $smallFont, $muted, 64, 944)

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()
Write-Host "Wrote $Output"

