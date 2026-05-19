"""
main.py
Run the comparison between Surya-Siddhanta and JPL ephemeris.
"""

import pandas as pd
import numpy as np
from surya_siddhanta import true_longitude

# Load JPL data
jpl = pd.read_csv('../data/jpl_ephemeris.csv')
jpl['date'] = pd.to_datetime('1900-01-01') + pd.to_timedelta(jpl.index, unit='D')

# Compute Surya-Siddhanta longitudes for the same JD
planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn']
results = pd.DataFrame(index=jpl.index)
results['jd'] = jpl['jd']

for planet in planets:
    ss_lon = [true_longitude(planet, jd) for jd in jpl['jd']]
    results[planet + '_ss'] = ss_lon
    results[planet + '_jpl'] = jpl[planet + '_lon']

# Compute residuals
for planet in planets:
    diff = (results[planet + '_ss'] - results[planet + '_jpl']) % 360
    diff = diff.where(diff <= 180, diff - 360)
    results[planet + '_residual'] = diff

# Summary statistics
stats = {}
for planet in planets:
    res = results[planet + '_residual']
    stats[planet] = {
        'mean_error': np.mean(np.abs(res)),
        'std_dev': np.std(res),
        'max_error': np.max(np.abs(res))
    }

stats_df = pd.DataFrame(stats).T
stats_df.to_csv('../results/summary_statistics.csv')
print("Statistics saved to results/summary_statistics.csv")
print(stats_df)
