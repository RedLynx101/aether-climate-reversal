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

function New-Canvas([int]$Width = 1400, [int]$Height = 900) {
    $bmp = New-Object System.Drawing.Bitmap $Width, $Height
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.Clear([System.Drawing.Color]::FromArgb(250,250,248))
    return @($bmp, $g)
}

function Draw-Title($g, [string]$Title, [string]$Subtitle) {
    $titleFont = New-Object System.Drawing.Font("Arial", 30, [System.Drawing.FontStyle]::Bold)
    $subFont = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Regular)
    $g.DrawString($Title, $titleFont, [System.Drawing.Brushes]::Black, 70, 42)
    $g.DrawString($Subtitle, $subFont, [System.Drawing.Brushes]::DimGray, 72, 88)
    $titleFont.Dispose(); $subFont.Dispose()
}

function Draw-Footer($g, [string]$Text, [int]$Height = 900) {
    $font = New-Object System.Drawing.Font("Arial", 12)
    $g.DrawString($Text, $font, [System.Drawing.Brushes]::DimGray, 70, $Height - 45)
    $font.Dispose()
}

function Draw-HBarChart($Path, $Rows, [string]$Title, [string]$Subtitle, [string]$Footer, [bool]$LogScale = $false, [double]$MinLog = 0) {
    $canvas = New-Canvas
    $bmp = $canvas[0]; $g = $canvas[1]
    Draw-Title $g $Title $Subtitle
    $labelFont = New-Object System.Drawing.Font("Arial", 15)
    $valueFont = New-Object System.Drawing.Font("Arial", 14, [System.Drawing.FontStyle]::Bold)
    $axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(120,120,120), 2)
    $gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(225,225,220), 1)
    $barBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(42, 104, 130))
    $left = 430; $top = 155; $barH = 54; $gap = 32; $maxW = 780
    $values = @($Rows | ForEach-Object {[double]$_.value})
    if ($LogScale) {
        $max = [Math]::Log10(($values | Measure-Object -Maximum).Maximum)
        $scaleLabel = "log10 scale"
    } else {
        $max = ($values | Measure-Object -Maximum).Maximum
        $scaleLabel = "linear scale"
    }
    $g.DrawLine($axisPen, $left, $top - 18, $left, $top + ($barH + $gap) * $Rows.Count - $gap + 8)
    for ($i=0; $i -le 4; $i++) {
        $x = $left + ($maxW * $i / 4)
        $g.DrawLine($gridPen, $x, $top - 18, $x, $top + ($barH + $gap) * $Rows.Count - $gap + 8)
    }
    for ($i=0; $i -lt $Rows.Count; $i++) {
        $r = $Rows[$i]
        $v = [double]$r.value
        $y = $top + $i * ($barH + $gap)
        $barValue = if ($LogScale) { [Math]::Max(0, [Math]::Log10($v) - $MinLog) } else { $v }
        $denom = if ($LogScale) { [Math]::Max(0.0001, $max - $MinLog) } else { $max }
        $w = [Math]::Max(2, $maxW * $barValue / $denom)
        $g.DrawString([string]$r.label, $labelFont, [System.Drawing.Brushes]::Black, 70, $y + 13)
        $g.FillRectangle($barBrush, $left, $y, [float]$w, $barH)
        $g.DrawString([string]$r.display, $valueFont, [System.Drawing.Brushes]::Black, [float]($left + $w + 16), $y + 14)
    }
    $scaleFont = New-Object System.Drawing.Font("Arial", 12)
    $g.DrawString($scaleLabel, $scaleFont, [System.Drawing.Brushes]::DimGray, $left, 812)
    Draw-Footer $g $Footer
    Save-Png $bmp $Path
    $scaleFont.Dispose(); $labelFont.Dispose(); $valueFont.Dispose(); $axisPen.Dispose(); $gridPen.Dispose(); $barBrush.Dispose(); $g.Dispose(); $bmp.Dispose()
}

$scenarios = Import-Csv (Join-Path $TableDir "aether_scenario_summary.csv")
$energyRows = @(
    @{label="Near-thermo capture"; value=($scenarios | Where-Object scenario -eq "near_thermo_capture_storage_100Gt").total_energy_twh_y; display="27,778 TWh/y"},
    @{label="Advanced capture"; value=($scenarios | Where-Object scenario -eq "advanced_capture_storage_100Gt").total_energy_twh_y; display="83,333 TWh/y"},
    @{label="Current DAC-like"; value=($scenarios | Where-Object scenario -eq "current_DAC_like_100Gt").total_energy_twh_y; display="222,222 TWh/y"},
    @{label="Advanced + 25% split"; value=($scenarios | Where-Object scenario -eq "advanced_capture_25pct_split_100Gt").total_energy_twh_y; display="145,427 TWh/y"},
    @{label="Advanced + 100% split"; value=($scenarios | Where-Object scenario -eq "advanced_capture_100pct_split_100Gt").total_energy_twh_y; display="331,708 TWh/y"}
)
Draw-HBarChart (Join-Path $FigureDir "energy_by_pathway_100gt.png") $energyRows "AETHER Energy Demand at 100 GtCO2/year" "Full CO2 splitting is a large energy penalty, not the default pathway." "Source: aether_scenario_model.py, generated 2026-06-09." $false 0

$storageRows = @(
    @{label="CO2 gas at STP"; value=50505; display="50,505 km3/y"},
    @{label="Supercritical CO2"; value=166.7; display="166.7 km3/y"},
    @{label="Liquid O2 if split"; value=63.7; display="63.7 km3/y"},
    @{label="Solid carbon if split"; value=12.4; display="12.4 km3/y"}
)
Draw-HBarChart (Join-Path $FigureDir "storage_state_volumes_100gt.png") $storageRows "Storage-State Volumes at 100 GtCO2/year" "Dense storage helps, but CO2 splitting buys compact carbon at a high energy cost." "Source: aether_scenario_model.py, generated 2026-06-09. Horizontal axis uses log10 volume." $true 0

$rebound = Import-Csv (Join-Path $TableDir "aether_jevons_rebound_sensitivity.csv")
$reboundRows = @($rebound | ForEach-Object { @{label=(([double]$_.jevons_or_policy_rebound_fraction_of_gross_removal).ToString("P0")); value=([double]$_.net_removal_gtco2_y + 42.2); display=(([double]$_.net_removal_gtco2_y).ToString("0.0") + " Gt net") } })
Draw-HBarChart (Join-Path $FigureDir "jevons_rebound_sensitivity_100gt.png") $reboundRows "Jevons and Policy Rebound Sensitivity" "Cheap removal fails if it induces enough new emissions or delayed abatement." "Source: aether_transition_model.py. Bar length is shifted for display; labels show net removal." $false 0

$robots = Import-Csv (Join-Path $TableDir "aether_robot_fleet_requirements.csv")
$robotRows = @($robots | ForEach-Object { @{label=($_.robots_per_mtco2_y_capacity_assumption + " robots/Mt capacity"); value=[double]$_.implied_aether_robot_fleet; display=(([double]$_.implied_aether_robot_fleet / 1000000).ToString("0.#") + "M robots") } })
Draw-HBarChart (Join-Path $FigureDir "robot_fleet_requirements_100gt.png") $robotRows "Robot Fleet Scale for 100 GtCO2/year" "AETHER is plausible only if robotics scales as an industrial supply chain, not as a demo category." "Source: aether_transition_model.py. Horizontal axis uses log10 fleet size." $true 5

& (Join-Path $Root "scripts\make_aether_rebound_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_carbon_cycle_figure.ps1") | Out-Null
Get-ChildItem -Path $FigureDir -Filter "*.png" | Select-Object FullName,Length
& (Join-Path $Root "scripts\make_aether_pathway_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_pathway_source_range_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_robotics_evidence_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_conversion_ledger_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_technology_acceleration_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_power_system_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_air_contactor_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_integrated_figures.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_deployment_timepath_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_storage_lifecycle_figures.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_regional_storage_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_material_supply_chain_figure.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_uncertainty_figures.ps1") | Out-Null
& (Join-Path $Root "scripts\make_aether_cost_stack_figures.ps1") | Out-Null


























































& (Join-Path $Root "scripts\make_aether_feasibility_scorecard_figure.ps1") | Out-Null
& (Join-Path $PSScriptRoot "make_aether_mrv_credit_integrity_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_climate_response_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_uncertainty_distribution_evidence_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_lifecycle_emissions_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_clean_energy_additionality_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_clean_power_deliverability_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_regional_power_dispatch_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_climate_emulator_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_fair_readiness_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_fair_forcing_execution_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_species_emissions_handoff_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_robotics_productivity_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_robotics_production_verification_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_robotics_field_productivity_distribution_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_state_dependent_carbon_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_correlated_uncertainty_figure.ps1")
& (Join-Path $PSScriptRoot "make_aether_adversarial_review_figure.ps1")

