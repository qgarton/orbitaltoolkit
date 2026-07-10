### utils.py
# Created 7/10/2026
# Author: Quaid Garton
# Last updated: 7/10/2026

# Contains utility functions for the orbital toolkit
### Current functions
# parse_horizons_csv() 
# takes horizons.csv and returns clean dataclass


from dataclasses import dataclass
import numpy as np

@dataclass
class Ephemeris:
    jd: np.ndarray
    dates: list
    states: np.ndarray

def parse_horizons_csv(filepath):
    # takes horizons.csv and returns clean dataclass
    state = np.loadtxt(filepath, delimiter=',', skiprows=3, usecols=range(2,8))

    with open(filepath) as f:
        lines = f.readlines()[3:]
    jd = np.array([float(line.split(',')[0]) for line in lines])
    dates = [line.split(',')[1][1:17] for line in lines] # [1:17] Removes 00:00:00... from dates
    return Ephemeris(jd=jd, dates=dates, states=state)

if __name__ == '__main__':
  print("\nutils.py is a library module. Run 'python3 test_utils.py' to test.\n" \
    "Or call parse_horizons_csv(filepath) to return ephemeris data")