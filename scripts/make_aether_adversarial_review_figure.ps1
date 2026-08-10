param(
    [string]$PanelsPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "analysis\tables\aether_adversarial_review_panels.csv"),
    [string]$Output = (Join-Path (Split-Path -Parent $PSScriptRoot) "analysis\figures\adversarial_review_risk_register.png")
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$rows = @(Import-Csv -LiteralPath $PanelsPath | Sort-Object {[int]$_.panel_order})
$width = 1600
$height = 960
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::FromArgb(250, 250, 248))

$titleFont = New-Object System.Drawing.Font("Segoe UI Semibold", 30)
$subtitleFont = New-Object System.Drawing.Font("Segoe UI", 15)
$labelFont = New-Object System.Drawing.Font("Segoe UI Semibold", 13)
$smallFont = New-Object System.Drawing.Font("Segoe UI", 10)
$axisFont = New-Object System.Drawing.Font("Segoe UI", 11)
$titleBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(28, 35, 43))
$mutedBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(84, 92, 101))
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(220, 224, 226), 1)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(122, 130, 138), 1)
$riskBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(190, 78, 69))
$maturityBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(42, 143, 128))
$lineBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(235, 165, 74))

$g.DrawString("AETHER Adversarial Review Register", $titleFont, $titleBrush, 56, 42)
$g.DrawString("What a serious reviewer can attack now, and which tests decide whether the paper must be narrowed.", $subtitleFont, $mutedBrush, 58, 88)

$labelX = 60
$plotX = 540
$plotY = 150
$plotW = 790
$rowH = 76
$barH = 18
$maxScore = 5.0

for ($tick = 0; $tick -le 5; $tick++) {
    $x = $plotX + ($tick / $maxScore) * $plotW
    $g.DrawLine($gridPen, [float]$x, [float]($plotY - 20), [float]$x, [float]($plotY + $rows.Count * $rowH + 8))
    $g.DrawString([string]$tick, $axisFont, $mutedBrush, [float]($x - 4), [float]($plotY - 42))
}
$g.DrawString("risk score", $axisFont, $mutedBrush, $plotX, 112)
$g.DrawString("evidence maturity", $axisFont, $mutedBrush, $plotX + 130, 112)
$g.FillRectangle($riskBrush, $plotX + 96, 118, 24, 11)
$g.FillRectangle($maturityBrush, $plotX + 242, 118, 24, 11)

for ($i = 0; $i -lt $rows.Count; $i++) {
    $row = $rows[$i]
    $y = $plotY + $i * $rowH
    $panelLabel = ([string]$row.reviewer_panel).Replace("_", " ")
    $discipline = [string]$row.discipline
    $risk = [double]$row.risk_score
    $maturity = [double]$row.evidence_maturity_score

    $g.DrawString($panelLabel, $labelFont, $titleBrush, $labelX, $y)
    $g.DrawString($discipline, $smallFont, $mutedBrush, $labelX, $y + 25)

    $riskW = ($risk / $maxScore) * $plotW
    $maturityW = ($maturity / $maxScore) * $plotW
    $g.FillRectangle($riskBrush, [float]$plotX, [float]($y + 8), [float]$riskW, [float]$barH)
    $g.FillRectangle($maturityBrush, [float]$plotX, [float]($y + 36), [float]$maturityW, [float]$barH)
    $g.DrawString($risk.ToString("0"), $smallFont, $titleBrush, [float]($plotX + $riskW + 8), [float]($y + 5))
    $g.DrawString($maturity.ToString("0"), $smallFont, $titleBrush, [float]($plotX + $maturityW + 8), [float]($y + 33))
}

$rightX = 1360
$g.DrawLine($axisPen, $rightX, 146, $rightX, 760)
$g.DrawString("Decision rule", $labelFont, $titleBrush, $rightX + 24, 150)
$decisionText = "High risk is acceptable at this stage only if it is paired with an explicit falsification test. If a P0 test fails, AETHER should narrow the claim instead of hiding the failure inside optimism."
$g.DrawString($decisionText, $smallFont, $mutedBrush, (New-Object System.Drawing.RectangleF ($rightX + 24), 182, 190, 190))
$g.FillRectangle($lineBrush, $rightX + 24, 404, 124, 12)
$g.DrawString("P0 tests decide core claims", $smallFont, $titleBrush, $rightX + 24, 422)
$g.FillRectangle($riskBrush, $rightX + 24, 478, 124, 12)
$g.DrawString("Risk before evidence upgrade", $smallFont, $titleBrush, $rightX + 24, 496)
$g.FillRectangle($maturityBrush, $rightX + 24, 552, 124, 12)
$g.DrawString("Evidence maturity today", $smallFont, $titleBrush, $rightX + 24, 570)

$note = "Interpretation: this is a reviewer-facing risk register, not a proof of readiness. The useful result is discipline: carbon-cycle, energy, storage, MRV, robotics, economics, process, and governance claims each receive a decisive next test."
$g.DrawString($note, $subtitleFont, $mutedBrush, (New-Object System.Drawing.RectangleF 58, 812, 1450, 58))
$g.DrawString("Source: aether_adversarial_review_model.py, generated from the current AETHER model suite and review-readiness backlog.", $smallFont, $mutedBrush, 58, 904)

$outDir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$bitmap.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bitmap.Dispose()

Write-Host "Wrote $Output"

