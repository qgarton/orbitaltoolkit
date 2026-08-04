### example_earth2mars_porkchop_plotter.py
# Created 7/9/2026
# Author: Quaid Garton
# Last updated: 7/9/2026

# Tests the porkchop_plotter.py function using known values from ASEN 5050 HW
from pathlib import Path
from orbitkit.ephem_io import parse_horizons_csv
from orbitkit.porkchop_plotter import porkchop_grid_calculation, plot_porkchops
from orbitkit.lambert import lambert

def earth2mars_porckchop_plotter():
    muSun = 1.32712428e11  # [km^3/s^2]
    # ============================================================
    # Example 1 — Earth to Mars
    ## Source: From ASEN 5050 HW6 problem 2, CU Boulder, Fall 2021
    # Comparable to previously created porkchop plots from MATLAB
    # ============================================================
    script_dir = Path(__file__).resolve().parent   # orbitaltoolkit/examples
    data_path_earth = script_dir.parent / "docs" / "examples" / "HW6_Ephem_Earth.txt"  # ..orbitaltoolkit/docs/examples/ephem_test.txt
    data_path_mars = script_dir.parent / "docs" / "examples" / "HW6_Ephem_Mars.txt"  # ..orbitaltoolkit/docs/examples/ephem_test.txt
    earth_data = parse_horizons_csv(data_path_earth)
    earth_data.name = "Earth"
    mars_data = parse_horizons_csv(data_path_mars)
    mars_data.name = "Mars"

    dV1, dV2 = porkchop_grid_calculation(earth_data, mars_data, muSun, lambert)
    plot_porkchops(earth_data, mars_data, dV1, dV2)

if __name__ == '__main__':
    earth2mars_porckchop_plotter()