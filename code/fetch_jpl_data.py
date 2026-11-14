"""Generate daily geocentric ecliptic longitudes with JPL DE432s via Astropy.

DE432s is a compact JPL kernel intended for dates from 1950 through 2050.
This script writes the actual ephemeris identifier and UTC dates with the data.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import astropy.units as u
from astropy.coordinates import GeocentricMeanEcliptic, get_body, solar_system_ephemeris
from astropy.time import Time

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "jpl_ephemeris.csv"
PLANETS = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"]


def main() -> None:
    start = Time("1950-01-01 00:00:00", scale="tdb")
    end = Time("2050-01-01 00:00:00", scale="tdb")
    day_offsets = np.arange(0, (end - start).to_value(u.day), 1.0)
    times = start + day_offsets * u.day

    data: dict[str, object] = {
        "jd": times.jd,
        "date_utc": times.utc.isot,
        "ephemeris": np.full(times.size, "DE432s"),
        "coordinate_convention": np.full(times.size, "apparent_geocentric_ecliptic_of_date"),
    }

    # get_body returns a geocentric GCRS SkyCoord; transform it explicitly to
    # the geocentric mean ecliptic frame at each observation epoch.
    with solar_system_ephemeris.set("de432s"):
        for planet in PLANETS:
            apparent_gcrs = get_body(planet, times)
            ecliptic_of_date = apparent_gcrs.transform_to(
                GeocentricMeanEcliptic(equinox=times)
            )
            data[f"{planet}_lon"] = ecliptic_of_date.lon.to_value(u.deg)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(data)
    frame.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(frame):,} daily rows to {OUTPUT}")
    print("Ephemeris: JPL DE432s; interval: 1950-01-01 through 2049-12-31")


if __name__ == "__main__":
    main()
