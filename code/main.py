"""Compare the simplified model with the generated DE432s reference CSV.

Run from the repository root:
    python code/fetch_jpl_data.py
    python code/main.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from analysis_utils import angular_residual_deg, summarize_residuals
from surya_siddhanta import true_longitude

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "jpl_ephemeris.csv"
OUTPUT = ROOT / "results"
PLANETS = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"]


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(
            f"Missing {INPUT}. First run: python code/fetch_jpl_data.py"
        )

    reference = pd.read_csv(INPUT)
    required = {"jd", *(f"{planet}_lon" for planet in PLANETS)}
    missing = sorted(required.difference(reference.columns))
    if missing:
        raise SystemExit(f"Input CSV is missing required columns: {', '.join(missing)}")

    results = reference[[column for column in ["jd", "date_utc"] if column in reference]].copy()
    summary: dict[str, dict[str, float | int]] = {}

    for planet in PLANETS:
        model = np.asarray(
            [true_longitude(planet, jd) for jd in reference["jd"].to_numpy(dtype=float)],
            dtype=float,
        )
        observed = reference[f"{planet}_lon"].to_numpy(dtype=float)
        residual = angular_residual_deg(model, observed)
        results[f"{planet}_simplified_deg"] = model
        results[f"{planet}_de432s_deg"] = observed
        results[f"{planet}_residual_deg"] = residual
        summary[planet] = summarize_residuals(residual)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT / "daily_residuals.csv", index=False)
    summary_frame = pd.DataFrame.from_dict(summary, orient="index")
    summary_frame.index.name = "planet"
    summary_frame.to_csv(OUTPUT / "summary_statistics.csv")
    print("Wrote results/daily_residuals.csv and results/summary_statistics.csv")
    print(summary_frame.to_string())


if __name__ == "__main__":
    main()
