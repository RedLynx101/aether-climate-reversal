"""Export source-linked public evidence and figures. --check fails on drift."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REGIONAL = "analysis/tables/aether_regional_reference_summary.json"
ATMOSPHERE = "data/parameters/atmospheric_reference.json"
INPUTS = [REGIONAL, ATMOSPHERE, "data/regional-reference/parameters.csv", "data/regional-reference/scenarios.json"]


def artifacts() -> dict[str, bytes]:
    regional = json.loads((ROOT / REGIONAL).read_text(encoding="utf-8"))
    atmosphere = json.loads((ROOT / ATMOSPHERE).read_text(encoding="utf-8"))
    atmosphere.update({
        "dryAirPercent": atmosphere["current"] / 10000,
        "referenceRatio": atmosphere["current"] / atmosphere["preindustrial"],
        "gapPpm": atmosphere["current"] - atmosphere["preindustrial"],
        "reductionPercent": (1 - atmosphere["preindustrial"] / atmosphere["current"]) * 100,
    })
    payload = {
        "version": "0.46", "sourceHashEncoding": "UTF-8 with canonical LF line endings", "sourceHashes": {p: hashlib.sha256((ROOT/p).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for p in INPUTS},
        "atmosphere": atmosphere, "metadata": regional["metadata"],
        "cases": regional["summary"], "failures": regional["failure_cases"],
        "resources": regional["resource_ledger"], "utility": regional["utility_ledger"],
        "climateStatus": "Absolute concentration and temperature projections quarantined: failed off-reference baseline diagnostic.",
    }
    outputs = {"website/app/evidence.generated.json": (json.dumps(payload, indent=2, allow_nan=False)+"\n").encode()}
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11, "axes.spines.top":False,
        "axes.spines.right":False, "axes.labelcolor":"#153e32", "text.color":"#153e32",
        "axes.edgecolor":"#94aaa0", "savefig.facecolor":"#f4f7f1"})
    cases = regional["summary"]

    def save(name: str, fig) -> None:
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", dpi=180, bbox_inches="tight", metadata={"Software":"AETHER public evidence exporter"})
        plt.close(fig)
        for folder in ("analysis/figures", "website/public/charts"):
            outputs[f"{folder}/{name}.png"] = buffer.getvalue()

    fig, ax = plt.subplots(figsize=(10,5), facecolor="#f4f7f1")
    labels = ["Gross\ncaptured", "Gross\nstored", "Physically\nretained", "Net of project\nemissions", "Risk-adjusted\ncredits"]
    fields = ["gross_capture_tco2_y", "gross_stored_tco2_y", "retained_tco2_y", "net_retained_tco2e_y", "risk_adjusted_credits_tco2e_y"]
    x = np.arange(len(fields))
    for n, (case, color) in enumerate(zip(cases, ["#78988a", "#175840"])):
        bars = ax.bar(x+(n-.5)*.34, [case[f]/1000 for f in fields], .34, color=color, label=["Ordinary", "Automation-assisted"][n])
        ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=9)
    ax.set_xticks(x, labels); ax.set_ylim(0,1100)
    ax.set_ylabel("Thousand tonnes/year (CO₂; net and credits in CO₂e)")
    ax.set_title("One process, two assumed operating cases", loc="left", fontweight="bold", pad=20)
    ax.legend(frameon=False, loc="upper left", ncols=2)
    ax.grid(axis="y", alpha=.15); ax.set_axisbelow(True)
    save("regional-carbon-ledger", fig)

    fig, ax = plt.subplots(figsize=(10,4.8), facecolor="#f4f7f1")
    for n, case in enumerate(cases):
        rows = [r for r in regional["resource_ledger"] if r["scenario_id"] == case["scenario_id"]]
        ax.plot(["Nameplate", "Uptime", "Electricity", "Thermal proxy", "Storage", "Budget"],
            [r["maximum_gross_capture_tco2_y"]/1000 for r in rows], marker="o", linewidth=2,
            color=["#78988a", "#175840"][n], label=["Ordinary", "Automation-assisted"][n])
    ax.set_ylim(700,1150); ax.set_ylabel("Supported gross capture (thousand tCO₂/year)")
    ax.set_title("The lowest limit sets annual output", loc="left", fontweight="bold", pad=20)
    ax.legend(frameon=False); ax.grid(axis="y", alpha=.2)
    save("regional-resource-limits", fig)

    fig, ax = plt.subplots(figsize=(10,4.7), facecolor="#f4f7f1")
    for n, case in enumerate(cases):
        rows = [r for r in regional["utility_ledger"] if r["scenario_id"] == case["scenario_id"] and r["ledger_section"] == "cash_source"]
        bottom=0
        for row, color, label in zip(rows,["#175840", "#89ac97"],["Current-load settlements", "Separate legacy funding"]):
            amount=row["amount"]/1e6
            ax.bar(n*3,amount,bottom=bottom,color=color,label=label if n==0 else None)
            ax.text(n*3,bottom+amount/2,f"${amount:.0f}m",ha="center",va="center",color="white" if bottom==0 else "#153e32")
            bottom+=amount
        use=case["total_uses_usd_y"]/1e6
        ax.bar(n*3+1,use,color="#b3b9a5",label="All modeled annual uses" if n==0 else None)
        ax.text(n*3+1,use+5,f"${use:.1f}m",ha="center")
    ax.set_xticks([0,1,3,4],["Ordinary\nsources","Ordinary\nuses","Assisted\nsources","Assisted\nuses"])
    ax.set_ylim(0,390); ax.set_ylabel("Million USD/year (illustrative assumptions)")
    ax.set_title("Current service does not finance all historical drawdown",loc="left",fontweight="bold",pad=20)
    ax.legend(frameon=False,loc="upper left",fontsize=9,ncols=2)
    ax.grid(axis="y",alpha=.15); ax.set_axisbelow(True)
    save("regional-funding-ledger",fig)
    return outputs


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    for relative, content in artifacts().items():
        path=ROOT/relative
        if args.check:
            if not path.exists() or path.read_bytes()!=content:
                raise SystemExit(f"Public evidence drift: {relative}; run this exporter")
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(content)
    print("Public evidence and three figures verified" if args.check else "Exported public evidence and three figures")


if __name__=="__main__":
    main()
