### example_solar_system_simulator.py
# Created 7/14/2026
# Author: Quaid Garton
# Last updated: 7/15/2026

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import re
from pathlib import Path

from orbitkit.ephem_io import parse_horizons_vectors
from orbitkit.constants import planet_params

def main():
        
    orbital_bodies = planet_params()

    script_dir = Path(__file__).resolve().parent   # orbitaltoolkit/tests/
    data_path = script_dir.parent / "docs" / "examples" / "solar_system_states" # ..orbitaltoolkit/
 
    ## Add initial conditions to all orbital bodies from ephemeris data, store full state data over time in state_vectors
    state_vectors = {}
    for body in orbital_bodies:
        filename = orbital_bodies[body]['name'] + "_ephem.txt"
        state = parse_horizons_vectors(data_path / filename) # Returns state in a dataclass
        orbital_bodies[body].update({'pos' : state.pos[0] , 'vel' : state.vel[0]})

        # Store data for later comparisons
        state_vectors.update({orbital_bodies[body]['name'] : state})

if __name__ == main():
    main()