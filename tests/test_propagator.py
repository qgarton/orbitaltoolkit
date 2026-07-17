### test_propagator.py
# Created 7/15/2026
# Author: Quaid Garton
# Last updated: 7/15/2026

import numpy as np
from pathlib import Path
import argparse
import time

from orbitkit.ephem_io import parse_horizons_vectors
from orbitkit.constants import planet_params
from orbitkit.propagator import propagate
from orbitkit.plotting import plot_plotly, plot_pyplot

def test_propagator(use_plotly=False, use_pyplot=False):
        
    orbital_bodies = planet_params()
    # Pick a few orbital bodies to simulate
    # keep = ['Sun' , 'Mercury', 'Venus', 'Earth', 'Moon', 'Mars']
    # orbital_bodies = {name : orbital_bodies[name] for name in keep}

    script_dir = Path(__file__).resolve().parent   # orbitaltoolkit/tests (.parent makes it the folder, next line removes /tests)
    data_path = script_dir.parent / "docs" / "examples" / "solar_system_states" # ..orbitaltoolkit
    
    ## Add initial conditions to all orbital bodies from ephemeris data, store full state data over time in horizons_data
    horizons_data = {}
    for body in orbital_bodies.keys():
        filename = body + "_ephem.txt"
        state = parse_horizons_vectors(data_path / filename) # Returns state in a dataclass
        orbital_bodies[body].update({'pos' : state.pos[0] , 'vel' : state.vel[0]})

        # Store ephemeris dataclass for later comparisons
        horizons_data.update({body : state}) # Type/size: 'list' (n_days+1,3)

    # Quick check that Sun has same time stamps as all other files
    for body in orbital_bodies:
        assert np.allclose(horizons_data[body].jd, horizons_data['Sun'].jd), \
            f"{body} ephemeris timestamps don't match Sun's"
        
    # Create tspan as full length of ephemeris files
    n_days = int(horizons_data['Sun'].jd[-1] - horizons_data['Sun'].jd[0])  # Currently 1 year
    years = 1
    tfin = n_days * 24 * 3600 * years # [sec]
    
    # Initialize special inputs and integrate
    tspan = (0, tfin)
    t_eval = np.linspace(tspan[0], tspan[1], (n_days+1) *years)
    start_integration = time.perf_counter()
    orbital_bodies = propagate(orbital_bodies, tspan, t_eval=t_eval, method='DOP853', show_progress=True) 
    print(f"Integration took {time.perf_counter()-start_integration} seconds")

    # Retrieve final Propagated values and view error table
    header = f"{'Body':<8} {'Pos err (km)':>12} {'Pos %':>8} {'Vel err (km/s)':>12} {'Vel %':>8}"
    row_fmt = "{:<8} {:>12.4f} {:>8.4f} {:>12.6f} {:>8.4f}"
    print(header)
    for body in orbital_bodies:
        pos_fin = orbital_bodies[body]['prop_pos'][:,-1]
        vel_fin = orbital_bodies[body]['prop_vel'][:,-1]
        error_pos = np.linalg.norm(pos_fin - horizons_data[body].pos[-1])
        error_vel = np.linalg.norm(vel_fin - horizons_data[body].vel[-1])
        rel_error_pos = np.linalg.norm(pos_fin - horizons_data[body].pos[-1])/np.linalg.norm(pos_fin)*100
        rel_error_vel = np.linalg.norm(vel_fin - horizons_data[body].vel[-1])/np.linalg.norm(vel_fin)*100
        print(row_fmt.format(body, error_pos, rel_error_pos, error_vel, rel_error_vel))
        
    if use_plotly:
        start_plotting = time.perf_counter()
        plot_plotly(orbital_bodies, orbital_bodies_truth_comparison=horizons_data, zoom_radius=6e9, zoom_height=2e9, animate=True)
        print(f"Plotting took {time.perf_counter()-start_plotting} seconds")
    if use_pyplot:
        plot_pyplot(orbital_bodies)

    # Check error in final value with pytest
    if __name__ != '__main__':
        for body in orbital_bodies:
            pos_fin = orbital_bodies[body]['prop_pos'][:,-1]
            vel_fin = orbital_bodies[body]['prop_vel'][:,-1]
            rel_error_pos = np.linalg.norm(pos_fin - horizons_data[body].pos[-1])/np.linalg.norm(pos_fin)*100
            rel_error_vel = np.linalg.norm(vel_fin - horizons_data[body].vel[-1])/np.linalg.norm(vel_fin)*100
            # 2% error may be large, but Mercury and pluto are always loosing accuracy at no fault of the propagator
            assert rel_error_pos < 2, f"{body} position error too large: {rel_error_pos:.4f} %"
            assert rel_error_vel < 2, f"{body} velocity error too large: {rel_error_vel:.6f} %"



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--plotly', action='store_true', help='Plot with Plotly (interactive)')
    parser.add_argument('--pyplot', action='store_true', help='Plot with Matplotlib (static)')
    args = parser.parse_args()

    test_propagator(use_plotly=args.plotly, use_pyplot=args.pyplot)