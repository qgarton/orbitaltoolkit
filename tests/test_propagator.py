### test_propagator.py
# Created 7/15/2026
# Author: Quaid Garton
# Last updated: 7/15/2026

import numpy as np
from pathlib import Path

from orbitkit.ephem_io import parse_horizons_vectors
from orbitkit.constants import planet_params
from orbitkit.propagator import propagate

def test_propagator():
        
    orbital_bodies = planet_params()
    # Pick a few orbital bodies to simulate
    keep = ['Sun' , 'Earth']
    orbital_bodies = {name : orbital_bodies[name] for name in keep}

    script_dir = Path(__file__).resolve().parent   # orbitaltoolkit/tests (.parent makes it the folder, next line removes /tests)
    data_path = script_dir.parent / "docs" / "examples" / "solar_system_states" # ..orbitaltoolkit
    
    ## Add initial conditions to all orbital bodies from ephemeris data, store full state data over time in state_vectors
    state_vectors = {}
    for body in orbital_bodies.keys():
        filename = body + "_ephem.txt"
        state = parse_horizons_vectors(data_path / filename) # Returns state in a dataclass
        orbital_bodies[body].update({'pos' : state.pos[0] , 'vel' : state.vel[0]})

        # Store ephemeris dataclass for later comparisons
        state_vectors.update({body : state})

    # Create tspan as full length of ephemeris files
    tfin = (state_vectors['Sun'].jd[-1] - state_vectors['Sun'].jd[0]) * 24 * 3600
    # Quick check that Sun has same time stamps as all other files
    for body in orbital_bodies:
        assert np.allclose(state_vectors[body].jd, state_vectors['Sun'].jd), \
            f"{body} ephemeris timestamps don't match Sun's"

    # Initialize special inputs and integrate
    tspan = (0, tfin)
    t_eval = np.linspace(tspan[0], tspan[1], 1000)
    orbital_bodies = propagate(orbital_bodies, tspan, t_eval, 'DOP853')

    # Retrieve final Propagated values and view error
    for body in orbital_bodies:
        pos_fin = orbital_bodies[body]['prop_pos'][:,-1]
        vel_fin = orbital_bodies[body]['prop_vel'][:,-1]
        error_pos = np.linalg.norm(pos_fin - state_vectors[body].pos[-1])
        error_vel = np.linalg.norm(vel_fin - state_vectors[body].vel[-1])
        print(f'Error in {body} = {error_pos:.4f} km and {error_vel:.6f} km/s')

    # Check error in final value with pytest
    if __name__ != '__main__':
        for body in orbital_bodies:
            pos_fin = orbital_bodies[body]['prop_pos'][:,-1]
            vel_fin = orbital_bodies[body]['prop_vel'][:,-1]
            assert error_pos < 100, f"{body} position error too large: {error_pos:.4f} km"
            assert error_vel < 0.01, f"{body} velocity error too large: {error_vel:.6f} km/s"



if __name__ == '__main__':
    test_propagator()