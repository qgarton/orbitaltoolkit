### test_porkchop_plotter.py
# Created 7/9/2026
# Author: Quaid Garton
# Last updated: 7/9/2026

# Tests the porkchop_plotter.py function using known values from ASEN 5050 HW
from pathlib import Path
from orbitkit.utils import parse_horizons_csv
from orbitkit.porkchop_plotter import porkchop_plotter
from orbitkit.lambert import lambert

def test_porkchop_plotter():
    muSun = 1.32712428e11  # [km^3/s^2]
    script_dir = Path(__file__).resolve().parent   # orbitaltoolkit/tests/
    data_path_earth = script_dir.parent / "docs" / "examples" / "HW6_Ephem_Earth.txt"  # ..orbitaltoolkit/docs/test/ephem_test.txt
    data_path_mars = script_dir.parent / "docs" / "examples" / "HW6_Ephem_Mars.txt"  # ..orbitaltoolkit/docs/test/ephem_test.txt
    earth_data = parse_horizons_csv(data_path_earth)
    mars_data = parse_horizons_csv(data_path_mars)

    porkchop_plotter(earth_data, mars_data, muSun, lambert)


    if __name__ != '__main__':
        print("assert somethin")
        # assert 


if __name__ == '__main__':
    test_porkchop_plotter()