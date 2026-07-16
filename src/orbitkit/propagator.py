### propagator.py
# Created 7/15/2026
# Author: Quaid Garton
# Last updated: 7/15/2026

# Numerically integrates gravitational dynamics of N bodies
## Assumptions:
# Point mass approximation
# No external forces (No drag, SRP, J2 effects, etc.)

import numpy as np
from scipy.integrate import solve_ivp
from orbitkit.constants import G


def propagate(orbital_bodies, tspan, t_eval, method='RK45', rtol=1e-9, atol=1e-12, dense_output=False):
    # Initialize state and tspan
    body_names = list(orbital_bodies.keys()) # Creates list of names in order
    y0 = np.concatenate([np.concatenate((orbital_bodies[name]['pos'], orbital_bodies[name]['vel'])) 
          for name in body_names])
    masses = np.array([orbital_bodies[name]['mass'] for name in body_names])

    # Call EOM with solve_ivp
    sol = solve_ivp(
    fun=EOM,                    # your derivative function: EOM(t, y) -> dy/dt
    t_span=(tspan[0], tspan[1]),            # start and end time
    y0=y0,                      # flat array: [x1,y1,z1,vx1,vy1,vz1, x2,y2,z2,...]
    method=method,              # integration scheme default 'RK45'
    t_eval=t_eval,              # optional: specific times to report output at
    args=(masses,),              # extra args passed to EOM after (t, y)
    rtol=rtol, atol=atol,       # error tolerances — this is what actually controls accuracy
    dense_output=dense_output,  # if True, gives a continuous interpolant you can call like sol.sol(t)
    )
    
    for i, body in enumerate(body_names):
        orbital_bodies[body].update({'prop_pos' : sol.y[6*i:6*i+3, :]})
        orbital_bodies[body].update({'prop_vel' : sol.y[6*i+3:6*i+6, :]})

    return orbital_bodies
    

def EOM(t,y,masses):
  # Calculate each 
    n = len(masses)
    dydt = np.zeros(len(y))
    for i in range(n):
        acc = np.zeros(3)
        for j in range(n):
            if j == i:
                continue
            r_vec = y[j*6:j*6+3] - y[i*6:i*6+3]     # Vector from i to j
            r_mag = np.linalg.norm(r_vec)           # Magnitude of distance
            acc += G * masses[j] / (r_mag**2) * (r_vec/r_mag) # Acceleration vector from i to j
        dydt[6*i:6*i+6] = np.concatenate((y[6*i+3:6*i+6], acc))
    return dydt



if __name__ == '__main__':
  print("\npropagator.py is a library module. Run 'python3 test_propagator.py' to test.\n"
    "Or call propagator.propagate() from another script to numerically integrate\n")