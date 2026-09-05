from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

ASSUMPTIONS = {
    "daccs_geologic": {
        "mrv_archetype": "regulated_geologic_storage",
        "measurement_discount_fraction": 0.02,
        "method_uncertainty_reserve_fraction": 0.01,
        "reversal_or_leakage_buffer_fraction": 0.03,
        "credit_invalidation_reserve_fraction": 0.02,
        "mrv_liability_cost_usd_tco2": 7.0,
        "risk_class": "lower_mrv_risk_high_durability",
        "source_keys": "epa_class_vi_wells_2026; epa_subpart_rr_mrv_2026; eu_crcf_2024; oxford_offsetting_principles_2024",
        "note": "Geologic DACCS has comparatively clear mass-balance and storage monitoring logic, but still needs buffers for measurement, leakage, and invalidated credits."
    },
    "enhanced_weathering": {
        "mrv_archetype": "geochemical_open_system",
        "measurement_discount_fraction": 0.12,
        "method_uncertainty_reserve_fraction": 0.10,
        "reversal_or_leakage_buffer_fraction": 0.08,
        "credit_invalidation_reserve_fraction": 0.08,
        "mrv_liability_cost_usd_tco2": 12.0,
        "risk_class": "medium_high_mrv_risk",
        "source_keys": "eu_crcf_2024; oxford_offsetting_principles_2024; state_of_cdr_2026",
        "note": "Weathering credit depends on reaction verification, transport, counterfactual baselines, runoff chemistry, and regional environmental constraints."
    },
    "ocean_alkalinity_enhancement": {
        "mrv_archetype": "ocean_geochemical_open_system",
        "measurement_discount_fraction": 0.15,
        "method_uncertainty_reserve_fraction": 0.15,
        "reversal_or_leakage_buffer_fraction": 0.10,
        "credit_invalidation_reserve_fraction": 0.10,
        "mrv_liability_cost_usd_tco2": 14.0,
        "risk_class": "high_mrv_risk_low_trl",
        "source_keys": "national_academies_ocean_cdr_2022; eu_crcf_2024; oxford_offsetting_principles_2024",
        "note": "Ocean alkalinity has large theoretical potential but open-ocean mixing, ecological risk, counterfactuals, and attribution make crediting harder than contained storage."
    },
    "beccs": {
        "mrv_archetype": "biomass_chain_plus_geologic_storage",
        "measurement_discount_fraction": 0.04,
        "method_uncertainty_reserve_fraction": 0.03,
        "reversal_or_leakage_buffer_fraction": 0.06,
        "credit_invalidation_reserve_fraction": 0.03,
        "mrv_liability_cost_usd_tco2": 8.0,
        "risk_class": "medium_mrv_risk",
        "source_keys": "epa_class_vi_wells_2026; epa_subpart_rr_mrv_2026; eu_crcf_2024",
        "note": "BECCS has durable geologic storage if captured, but biomass supply, land-use accounting, lifecycle emissions, and storage monitoring must all clear."
    },
    "biochar": {
        "mrv_archetype": "distributed_product_or_soil_storage",
        "measurement_discount_fraction": 0.10,
        "method_uncertainty_reserve_fraction": 0.08,
        "reversal_or_leakage_buffer_fraction": 0.20,
        "credit_invalidation_reserve_fraction": 0.08,
        "mrv_liability_cost_usd_tco2": 10.0,
        "risk_class": "medium_high_reversal_risk",
        "source_keys": "eu_crcf_2024; oxford_offsetting_principles_2024; state_of_cdr_2026",
        "note": "Biochar credit depends on feedstock, process conditions, product fate, soil/material application, and durability over decades to centuries."
    },
    "afforestation_reforestation": {
        "mrv_archetype": "land_biological_storage",
        "measurement_discount_fraction": 0.20,
        "method_uncertainty_reserve_fraction": 0.15,
        "reversal_or_leakage_buffer_fraction": 0.35,
        "credit_invalidation_reserve_fraction": 0.15,
        "mrv_liability_cost_usd_tco2": 12.0,
        "risk_class": "high_reversal_and_counterfactual_risk",
        "source_keys": "eu_crcf_2024; oxford_offsetting_principles_2024; state_of_cdr_2026",
        "note": "Land biological storage is important for climate and ecosystems, but fire, drought, land-use change, counterfactuals, and non-permanence make 100-year crediting fragile."
    },
    "direct_ocean_capture": {
        "mrv_archetype": "engineered_ocean_capture_plus_storage",
        "measurement_discount_fraction": 0.05,
        "method_uncertainty_reserve_fraction": 0.05,
        "reversal_or_leakage_buffer_fraction": 0.05,
        "credit_invalidation_reserve_fraction": 0.04,
        "mrv_liability_cost_usd_tco2": 10.0,
        "risk_class": "medium_mrv_risk_low_trl",
        "source_keys": "national_academies_ocean_cdr_2022; epa_subpart_rr_mrv_2026; eu_crcf_2024",
        "note": "Direct ocean capture may be more engineered than diffuse ocean alkalinity, but still needs source-backed ocean-attribution, storage, lifecycle, and ecological-risk accounting."
    },
}

def read_csv(name):
    with (TABLE_DIR / name).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))

def write_csv(name, rows, fieldnames):
    with (TABLE_DIR / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def f(value, digits=6):
    return f"{value:.{digits}f}"

def float_value(row, key):
    value = row.get(key, "")
    if value in ("", None):
        return 0.0
    return float(value)


def apply_mrv_credit_buffers(net_accounting_gtco2e_y, buffer_fractions):
    """Apply credit buffers only after physical-retention and lifecycle accounting."""
    if any(not 0.0 <= fraction <= 1.0 for fraction in buffer_fractions):
        raise ValueError("MRV buffer fractions must be between zero and one")
    multiplier = math.prod(1.0 - fraction for fraction in buffer_fractions)
    return multiplier, max(net_accounting_gtco2e_y, 0.0) * multiplier

portfolio = {row["pathway"]: row for row in read_csv("aether_pathway_portfolio_allocation.csv")}
lifecycle = {row["pathway"]: row for row in read_csv("aether_storage_lifecycle_routes.csv")}

assumption_rows = []
pathway_rows = []

for pathway, assumption in ASSUMPTIONS.items():
    p = portfolio[pathway]
    l = lifecycle[pathway]
    gross = float_value(p, "aether_optimized_allocation_gtco2_y")
    physically_retained = float_value(l, "physically_retained_after_100y_gtco2_y")
    lifecycle_emissions_proxy = float_value(l, "lifecycle_emissions_proxy_gtco2e_y")
    net_accounting_proxy = float_value(
        l, "net_after_retention_minus_lifecycle_proxy_gtco2e_y"
    )
    baseline_cost = float_value(p, "aether_optimized_cost_usd_tco2_assumption")
    retention_fraction = physically_retained / gross if gross else 0.0
    net_accounting_fraction = net_accounting_proxy / gross if gross else 0.0
    mrv_multiplier, creditable = apply_mrv_credit_buffers(
        net_accounting_proxy,
        [
            assumption["measurement_discount_fraction"],
            assumption["method_uncertainty_reserve_fraction"],
            assumption["reversal_or_leakage_buffer_fraction"],
            assumption["credit_invalidation_reserve_fraction"],
        ],
    )
    creditable_fraction = creditable / gross if gross else 0.0
    gross_to_creditable = 1.0 / creditable_fraction if creditable_fraction > 0.0 else None
    mrv_cost = assumption["mrv_liability_cost_usd_tco2"]
    annual_mrv_liability_cost_billion = gross * mrv_cost
    cost_per_creditable_tonne = (
        (baseline_cost + mrv_cost) / creditable_fraction
        if creditable_fraction > 0.0
        else None
    )

    assumption_rows.append({
        "pathway": pathway,
        "display_name": p["display_name"],
        "mrv_archetype": assumption["mrv_archetype"],
        "measurement_discount_fraction": f(assumption["measurement_discount_fraction"], 4),
        "method_uncertainty_reserve_fraction": f(assumption["method_uncertainty_reserve_fraction"], 4),
        "reversal_or_leakage_buffer_fraction": f(assumption["reversal_or_leakage_buffer_fraction"], 4),
        "credit_invalidation_reserve_fraction": f(assumption["credit_invalidation_reserve_fraction"], 4),
        "mrv_liability_cost_usd_tco2": f(mrv_cost, 2),
        "risk_class": assumption["risk_class"],
        "source_keys": assumption["source_keys"],
        "assumption_note": assumption["note"],
    })

    pathway_rows.append({
        "pathway": pathway,
        "display_name": p["display_name"],
        "gross_gtco2_y": f(gross, 3),
        "physically_retained_after_100y_gtco2_y": f(physically_retained, 3),
        "physical_retention_fraction": f(retention_fraction, 5),
        "lifecycle_emissions_proxy_gtco2e_y": f(lifecycle_emissions_proxy, 3),
        "net_after_retention_minus_lifecycle_proxy_gtco2e_y": f(net_accounting_proxy, 3),
        "net_accounting_proxy_fraction_of_gross": f(net_accounting_fraction, 5),
        "mrv_credit_multiplier_after_buffers": f(mrv_multiplier, 5),
        "creditable_gtco2e_y_after_mrv": f(creditable, 3),
        "creditable_fraction_of_gross": f(creditable_fraction, 5),
        "gross_to_creditable_multiplier": (
            f(gross_to_creditable, 3) if gross_to_creditable is not None else ""
        ),
        "gross_to_creditable_multiplier_status": (
            "defined_positive_credit" if gross_to_creditable is not None else "infeasible_zero_credit"
        ),
        "baseline_cost_usd_tco2_gross": f(baseline_cost, 2),
        "mrv_liability_cost_usd_tco2_gross": f(mrv_cost, 2),
        "annual_mrv_liability_cost_billion_usd": f(annual_mrv_liability_cost_billion, 2),
        "cost_usd_per_creditable_tco2_after_mrv": (
            f(cost_per_creditable_tonne, 2) if cost_per_creditable_tonne is not None else ""
        ),
        "risk_class": assumption["risk_class"],
        "source_keys": assumption["source_keys"],
        "accounting_boundary_note": "MRV buffers convert the separate retention-minus-lifecycle accounting proxy into provisional creditable CO2e; neither quantity is an automatic climate-flow claim.",
    })

gross_total = sum(float(row["gross_gtco2_y"]) for row in pathway_rows)
physically_retained_total = sum(float(row["physically_retained_after_100y_gtco2_y"]) for row in pathway_rows)
lifecycle_emissions_proxy_total = sum(float(row["lifecycle_emissions_proxy_gtco2e_y"]) for row in pathway_rows)
net_accounting_proxy_total = sum(
    float(row["net_after_retention_minus_lifecycle_proxy_gtco2e_y"])
    for row in pathway_rows
)
creditable_total = sum(float(row["creditable_gtco2e_y_after_mrv"]) for row in pathway_rows)
weighted_creditable_fraction = creditable_total / gross_total
gross_required_for_100_credit = (
    100.0 / weighted_creditable_fraction if weighted_creditable_fraction > 0.0 else None
)
additional_gross_required = (
    gross_required_for_100_credit - 100.0
    if gross_required_for_100_credit is not None
    else None
)
annual_mrv_cost_trillion = sum(float(row["annual_mrv_liability_cost_billion_usd"]) for row in pathway_rows) / 1000.0
annual_baseline_cost_trillion = sum(
    float(row["gross_gtco2_y"]) * float(row["baseline_cost_usd_tco2_gross"]) for row in pathway_rows
) / 1000.0
annual_cost_with_mrv_at_100_gross_trillion = annual_baseline_cost_trillion + annual_mrv_cost_trillion
annual_cost_for_100_credit_same_mix_trillion = (
    annual_cost_with_mrv_at_100_gross_trillion * (gross_required_for_100_credit / 100.0)
    if gross_required_for_100_credit is not None
    else None
)
credit_shortfall_after_mrv = 100.0 - creditable_total

summary_rows = [
    {
        "summary_id": "gross_portfolio",
        "metric": "AETHER portfolio gross removal before lifecycle or MRV filters",
        "value": f(gross_total, 3),
        "unit": "GtCO2/year",
        "interpretation": "The current pathway portfolio still starts at the 100 GtCO2/year gross target.",
    },
    {
        "summary_id": "physically_retained_100y",
        "metric": "Physical gross removal retained after 100 years under route assumptions",
        "value": f(physically_retained_total, 3),
        "unit": "GtCO2/year",
        "interpretation": "This is a physical-retention screen before lifecycle-emissions and MRV accounting debits.",
    },
    {
        "summary_id": "lifecycle_emissions_proxy",
        "metric": "Provisional lifecycle-emissions accounting debit",
        "value": f(lifecycle_emissions_proxy_total, 3),
        "unit": "GtCO2e/year",
        "interpretation": "This provisional CO2e proxy is not a time- or species-resolved climate flow.",
    },
    {
        "summary_id": "net_retention_minus_lifecycle_proxy",
        "metric": "Physical retention minus provisional lifecycle-emissions debit",
        "value": f(net_accounting_proxy_total, 3),
        "unit": "GtCO2e/year accounting proxy",
        "interpretation": "This scalar screen is the MRV input, not an issued credit or automatic climate outcome.",
    },
    {
        "summary_id": "mrv_creditable_total",
        "metric": "Provisional creditable removal after MRV, reversal, invalidation, and liability buffers",
        "value": f(creditable_total, 3),
        "unit": "GtCO2e/year creditable",
        "interpretation": "This is the current stress-test estimate for tonnes that should be treated as creditable under conservative accounting.",
    },
    {
        "summary_id": "gross_required_for_100_credit_same_mix",
        "metric": "Gross removal required for 100 GtCO2/year creditable removal at the same pathway mix",
        "value": (
            f(gross_required_for_100_credit, 3)
            if gross_required_for_100_credit is not None
            else ""
        ),
        "unit": "GtCO2/year gross",
        "interpretation": "AETHER must overbuild gross removal materially if credit integrity is enforced rather than assumed.",
    },
    {
        "summary_id": "additional_gross_required_vs_100",
        "metric": "Additional gross removal required above the nominal 100 GtCO2/year target",
        "value": f(additional_gross_required, 3) if additional_gross_required is not None else "",
        "unit": "GtCO2/year gross",
        "interpretation": "This is the penalty for treating gross tonnes, durable tonnes, and creditable tonnes as different quantities.",
    },
    {
        "summary_id": "annual_mrv_liability_cost_at_100_gross",
        "metric": "Annual MRV and liability reserve at 100 GtCO2/year gross under provisional assumptions",
        "value": f(annual_mrv_cost_trillion, 3),
        "unit": "trillion USD/year",
        "interpretation": "This is an added hard-floor bucket, not a replacement for capture, energy, transport, or storage costs.",
    },
    {
        "summary_id": "annual_cost_with_mrv_at_100_gross",
        "metric": "Portfolio annual cost including provisional MRV/liability at 100 GtCO2/year gross",
        "value": f(annual_cost_with_mrv_at_100_gross_trillion, 3),
        "unit": "trillion USD/year",
        "interpretation": "This combines current pathway portfolio cost assumptions with the MRV/liability reserve.",
    },
    {
        "summary_id": "annual_cost_for_100_credit_same_mix",
        "metric": "Portfolio annual cost for 100 GtCO2/year creditable removal at the same pathway mix",
        "value": (
            f(annual_cost_for_100_credit_same_mix_trillion, 3)
            if annual_cost_for_100_credit_same_mix_trillion is not None
            else ""
        ),
        "unit": "trillion USD/year",
        "interpretation": "This is a first estimate of the cost penalty if the target is creditable tonnes rather than gross tonnes.",
    },
    {
        "summary_id": "credit_shortfall_after_mrv",
        "metric": "Shortfall from 100 GtCO2/year after applying MRV and credit-integrity filters to the 100 Gt gross portfolio",
        "value": f(credit_shortfall_after_mrv, 3),
        "unit": "GtCO2/year creditable",
        "interpretation": "Without overbuild or a more durable pathway mix, the nominal 100 Gt gross portfolio is not a 100 Gt creditable-removal system.",
    },
]

for summary_row in summary_rows:
    if summary_row["summary_id"] in {
        "gross_required_for_100_credit_same_mix",
        "additional_gross_required_vs_100",
        "annual_cost_for_100_credit_same_mix",
    }:
        summary_row["calculation_status"] = (
            "defined_positive_credit"
            if gross_required_for_100_credit is not None
            else "infeasible_zero_credit"
        )
    else:
        summary_row["calculation_status"] = "reported"

write_csv(
    "aether_mrv_credit_integrity_assumptions.csv",
    assumption_rows,
    [
        "pathway",
        "display_name",
        "mrv_archetype",
        "measurement_discount_fraction",
        "method_uncertainty_reserve_fraction",
        "reversal_or_leakage_buffer_fraction",
        "credit_invalidation_reserve_fraction",
        "mrv_liability_cost_usd_tco2",
        "risk_class",
        "source_keys",
        "assumption_note",
    ],
)
write_csv(
    "aether_mrv_credit_integrity_by_pathway.csv",
    pathway_rows,
    [
        "pathway",
        "display_name",
        "gross_gtco2_y",
        "physically_retained_after_100y_gtco2_y",
        "physical_retention_fraction",
        "lifecycle_emissions_proxy_gtco2e_y",
        "net_after_retention_minus_lifecycle_proxy_gtco2e_y",
        "net_accounting_proxy_fraction_of_gross",
        "mrv_credit_multiplier_after_buffers",
        "creditable_gtco2e_y_after_mrv",
        "creditable_fraction_of_gross",
        "gross_to_creditable_multiplier",
        "gross_to_creditable_multiplier_status",
        "baseline_cost_usd_tco2_gross",
        "mrv_liability_cost_usd_tco2_gross",
        "annual_mrv_liability_cost_billion_usd",
        "cost_usd_per_creditable_tco2_after_mrv",
        "risk_class",
        "source_keys",
        "accounting_boundary_note",
    ],
)
write_csv(
    "aether_mrv_credit_integrity_summary.csv",
    summary_rows,
    ["summary_id", "metric", "value", "unit", "interpretation", "calculation_status"],
)

