# Sūrya-Siddhānta: exploratory computational analysis

This repository is an exploratory software project for examining simplified
planetary-longitude formulas alongside a modern ephemeris reference. It is
**not yet a complete computational reconstruction of the Sūrya-Siddhānta**,
and the present model should not be used to claim historical or astronomical
prediction accuracy.

The earlier repository description referred to a DE441 comparison over
1900–2025. The checked-in data generator actually uses Astropy with the JPL
DE432s kernel; this workflow is now explicitly limited to 1950–2049 and names
its coordinate convention in the generated CSV.

## Current implementation

- Constant mean daily motions and approximate reference longitudes.
- A simplified sinusoidal manda correction.
- A daily geocentric apparent longitude reference generated from DE432s.
- Circular angular-residual calculations that correctly wrap at 0°/360°.
- Descriptive residual summaries and automated invariant tests.

The theoretical implementation is deliberately labelled simplified. In
particular, the current code does not implement the complete traditional
sine-table procedure or all required planetary corrections. The manuscript
mentioned in an earlier README revision is not included here; this repository
is not presented as a standalone reproduction of its results.

## Reproduce the software comparison

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt

# Generate the reference ephemeris (downloads/caches the DE432s kernel)
python code/fetch_jpl_data.py

# Compare longitudes and write residuals/statistics
python code/main.py

# Run offline unit tests
python -m unittest discover -s tests -v
```

The fetch step needs network access the first time it downloads the DE432s
kernel. The generated daily CSV is intentionally not committed.

## Output files

- `data/jpl_ephemeris.csv` – date, Julian Day, ephemeris identifier,
  coordinate convention and geocentric ecliptic longitudes.
- `results/daily_residuals.csv` – model/reference longitude pairs and signed
  wrapped residuals for each planet.
- `results/summary_statistics.csv` – count, MAE, standard deviation, maximum
  absolute error, RMSE and mean signed error in degrees.

## Repository layout

```text
code/
  surya_siddhanta.py    # simplified theoretical model
  fetch_jpl_data.py     # Astropy / DE432s data generator
  analysis_utils.py     # circular residuals and metrics
  main.py               # reproducible comparison script
tests/
  test_analysis_utils.py
  test_surya_siddhanta.py
docs/
  model-audit.md        # methodological scope and required validation
```

## Important scientific limitations

The current model uses approximate constants and an incomplete correction
scheme. Coordinate-frame alignment, epoch conventions, time scales and the
sidereal/tropical reference must be independently verified before interpreting
residuals. The bīja/Kalman-filter analogy is a research hypothesis, not a
result established by this code.

Astropy documents `get_body` as returning apparent geocentric GCRS
coordinates; this project explicitly transforms those coordinates into the
geocentric mean ecliptic frame of date. Astropy documents DE432s as covering
1950–2050, which is why the generator uses that interval. See the [Astropy
get_body documentation](https://docs.astropy.org/en/stable/api/astropy.coordinates.get_body.html)
and [Astropy solar-system ephemeris documentation](https://docs.astropy.org/en/stable/coordinates/solarsystem.html).

The unit tests check software invariants. They do not validate the accuracy of
the simplified model against a critical edition or establish prediction
performance. A research-grade release needs primary-source equation
transcription, an independently verified coordinate convention, sensitivity
analysis, a versioned reference dataset and documented uncertainty.

## License

MIT. See [LICENSE](LICENSE).
