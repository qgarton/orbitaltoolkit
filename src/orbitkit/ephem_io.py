### ephem_io.py
# Created 7/10/2026
# Author: Quaid Garton
# Last updated: 7/15/2026

# Replaced utils.py
# Contains parsing functions for the orbital toolkit
### Current functions are horizons data parsers
# parse_horizons_csv() 
#   takes horizons.csv and returns clean dataclass
# parse_horizons_vectors()
#   takes horizons vector file and returns 


from dataclasses import dataclass
import numpy as np
import re

@dataclass
class Ephemeris:
    jd: np.ndarray
    date: list
    pos: np.ndarray
    vel: np.ndarray

def parse_horizons_csv(filepath):
# Input Filename/path horizons.csv and returns clean dataclass
    pos = np.loadtxt(filepath, delimiter=',', skiprows=3, usecols=range(2,5))
    vel = np.loadtxt(filepath, delimiter=',', skiprows=3, usecols=range(5,8))

    with open(filepath) as f:
        lines = f.readlines()[3:]
    jd = np.array([float(line.split(',')[0]) for line in lines])
    date = [line.split(',')[1][1:17] for line in lines] # [1:17] Removes 00:00:00... from date
    return Ephemeris(jd=jd, date=date, pos=pos, vel=vel)

def parse_horizons_vectors(filepath):
# Input Filename/path from JPL Horizons vector format, returns clean dataclass
# LT, RG, RR which are Light-Time, Range, and Range-Rate are currently not extracted
    # Set Pattern based on scientific notation
    FLOAT_PATTERN = re.compile(r"[-+]?\d*\.\d+(?:[eE][-+]?\d+)?")
    # Date pattern
    DATE_PATTERN = re.compile(r"(?<=\s)\d+-\w+-\d+")
    # Track all variables separately
    date, jd, pos, vel = [], [], [], []
    with open(filepath, mode="r", encoding="utf-8") as file:
        started = False
        for line in file:
            # Start at indicator
            if "$$SOE" in line:
                started = True
                continue
            # Stop at indicator
            if "$$EOE" in line:
                break
            # Collect data
            if started:
                # Strip white space to make matching with line start work
                stripped = line.strip()
                # Identify timestamp lines, pull jd for calculations and date for viewability
                if "TDB" in line:
                    jd_match = FLOAT_PATTERN.search(line)   # JD is the first float on this line
                    date_match = DATE_PATTERN.search(line)
                    if jd_match:
                        jd.append(float(jd_match.group()))
                    if date_match:
                        date.append(date_match.group())
                    continue
                # Identify and pull position vector
                if stripped.startswith("X"):
                    pos.append(tuple(float(v) for v in FLOAT_PATTERN.findall(line)))
                    continue
                # Identify and pull velocity vector
                if stripped.startswith("VX"):
                    vel.append(tuple(float(v) for v in FLOAT_PATTERN.findall(line)))
                    continue
                # LT/RG/RR line intentionally not captured    

    return Ephemeris(jd=jd, date=date, pos=pos, vel=vel)


if __name__ == '__main__':
  print("\nutils.py is a library module. Run 'python3 test_utils.py' to test.\n" \
    "Or call parse_horizons_csv(filepath) to return ephemeris data")