### test_porkchop_plotter.py
# Created 7/9/2026
# Author: Quaid Garton
# Last updated: 7/9/2026

# Tests the porkchop_plotter.py function using known values from ASEN 5050 HW
import numpy as np
from orbitkit.ephem_io import Ephemeris
from orbitkit.porkchop_plotter import porkchop_grid_calculation, plot_porkchops
from orbitkit.lambert import lambert

def test_porkchop_plotter():
    ## Tests plotter with fabricated data. currently contains missing portions due to 180 deg failure
    muSun = 1.32712428e11  # [km^3/s^2]

    dep_days = np.arange(-60, 121, 5)
    arr_days = np.arange(100, 390, 10)
    earth = make_synthetic_ephemeris(r_AU=1.0, period_days=365.25, phase0_deg=0.0, t_days_array=dep_days)
    mars  = make_synthetic_ephemeris(r_AU=1.524, period_days=686.98, phase0_deg=45.0, t_days_array=arr_days)

    # expected: grid minimum near dep_days≈0, arr_days≈260, total dV ≈ 5.60 km/s
    dV1, dV2 = porkchop_grid_calculation(earth, mars, muSun, lambert)
    if __name__ == '__main__':
        plot_porkchops(earth, mars, dV1, dV2)

    if __name__ != '__main__':
        print("assert somethin")
        # assert 

def make_synthetic_ephemeris(r_AU, period_days, phase0_deg, t_days_array, mu_sun=1.32712428e11):
    # Gives really nice data to make an expected shape porkchop plot
    AU = 1.495978707e8  # km
    r_mag = r_AU * AU
    n = 2*np.pi / (period_days*86400)
    v_mag = np.sqrt(mu_sun / r_mag)

    pos = np.zeros((len(t_days_array), 3))
    vel = np.zeros((len(t_days_array), 3))
    for i, td in enumerate(t_days_array):
        theta = np.radians(phase0_deg) + n*(td*86400)
        pos[i, :] = [r_mag*np.cos(theta), r_mag*np.sin(theta), 0.0]
        vel[i, :] = v_mag*np.array([-np.sin(theta), np.cos(theta), 0.0])

    date = [f"synthetic day {td}" for td in t_days_array]
    return Ephemeris(jd=np.array(t_days_array, dtype=float), date=date, pos=pos, vel=vel)

if __name__ == '__main__':
    test_porkchop_plotter()