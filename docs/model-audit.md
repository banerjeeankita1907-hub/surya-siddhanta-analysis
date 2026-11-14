# Scientific scope and reproducibility audit

## What the checked-in model currently does

The module in code/surya_siddhanta.py is a simplified numerical illustration. It
uses constant mean daily motions, a fixed reference Julian Day, approximate
mandocca values and a small sinusoidal correction. It explicitly omits the full
traditional sine-table procedure and the sighra correction for Mercury and
Venus. The implementation is not a complete reconstruction of the
Sūrya-Siddhānta and should not be described as one.

The analysis pipeline compares the simplified model with geocentric ecliptic
longitudes generated using Astropy's DE432s ephemeris. This is not DE441. The
comparison is a software exercise unless the coordinate frames, epochs,
time scales, planet-centre definitions and source equations are independently
verified and documented.

## Important limitations

- The model's epoch and constants are approximate and need primary-source
  verification before historical or astronomical claims are made.
- Constant mean motion plus the current correction is not a full planetary
  theory; the resulting residuals are not an accuracy claim for the ancient
  text as a whole.
- The generated comparison coordinates are geocentric ecliptic positions.
  Their frame and equinox must match the theoretical longitude convention.
- DE432s and DE441 are different ephemerides; reports must name the one actually
  used.
- The bīja/Kalman-filter analogy is a research hypothesis, not established by
  the existing implementation or tests.

## Reproducible workflow

1. Install the dependencies in requirements.txt.
2. Run code/fetch_jpl_data.py to generate data/jpl_ephemeris.csv from Astropy's
   configured DE432s kernel.
3. Run code/main.py to compare only the common columns and write residuals and
   descriptive statistics into results/.
4. Run the unit tests with python -m unittest discover -s tests -v.

The generated ephemeris file is intentionally not committed. Record dependency
versions and the generated file's checksum for a reproducible run.

## Research-grade next steps

Before submitting quantitative claims, replace placeholders with equations and
constants transcribed from a cited critical edition, include the complete
manda/sighra procedure, independently validate the Julian-day convention,
compare identical coordinate frames, test a versioned JPL reference over
multiple epochs, quantify uncertainty and sensitivity, and publish data plus
script versions. Tests in this repository verify implementation invariants;
they do not establish historical or astronomical accuracy.
