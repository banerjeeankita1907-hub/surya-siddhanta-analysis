"""
fetch_jpl_data.py
Uses astropy to download JPL DE441 ephemeris data and save planet positions as CSV.
"""

from astropy.coordinates import get_body_barycentric, solar_system_ephemeris
from astropy.time import Time
import numpy as np
import pandas as pd

# Set ephemeris to DE441 (requires jplephem and the ephemeris file)
# For simplicity, we use the built-in 'de432s' (DE440/441 not in astropy by default)
# The paper used HORIZONS batch; here we simulate with astropy.
solar_system_ephemeris.set('de432s')

start_jd = Time('1900-01-01 00:00:00', scale='tdb')
end_jd = Time('2026-01-01 00:00:00', scale='tdb')
days = np.arange((end_jd - start_jd).jd)
times = start_jd + days

planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn']

data = {'jd': times.jd}

for planet in planets:
    # Get heliocentric position; then convert to equatorial coordinates
    obj = get_body_barycentric(planet, times)
    # Just store the ecliptic longitude for comparison (simplified)
    # Real paper used equatorial; this is a placeholder.
    from astropy.coordinates import GCRS, SkyCoord
    coord = SkyCoord(obj.represent_as('cartesian').xyz.T, unit='au', frame='icrs')
    data[planet + '_lon'] = coord.geocentricmeanecliptic.lon.deg

df = pd.DataFrame(data)
df.to_csv('../data/jpl_ephemeris.csv', index=False)
print("JPL ephemeris saved to data/jpl_ephemeris.csv")
