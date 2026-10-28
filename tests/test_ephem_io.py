### test_ephem_io.py
# Created 7/10/2026
# Author: Quaid Garton
# Last updated 7/15/2026

# Replaced test_utils.py
# Tests ephem_io.py
### Current tests
# test_parse_horizons_csv()
# test_parse_horizons_vectors()
from pathlib import Path
from orbitkit.ephem_io import parse_horizons_csv, parse_horizons_vectors
import numpy as np

def test_parse_horizons_csv():
    # Tests data structure from horizons csv parser
    
    script_dir = Path(__file__).resolve().parent   # orbitaltoolkit/tests/
    data_path = script_dir.parent / "docs" / "tests" / "ephem_csv_test.txt"  # ..orbitaltoolkit/docs/test/ephem_test.txt
    earth_sample = parse_horizons_csv(data_path)
    # Print to verify visually
    print("\nCSV sample:\n",earth_sample)

    # Expected/desired data and form
    expected_jd = np.array([41.5, 43.5, 45.5, 47.5])
    expected_date = ['2005-Jun-20', '2005-Jun-22',
                       '2005-Jun-24', '2005-Jun-26']
    expected_pos = np.array([
        [-3.42, -1.51,  2.15],
        [ 1.63, -1.52,  2.26],
        [ 6.69, -1.51,  2.28],
        [ 1.17, -1.51,  2.2 ]
    ])
    expected_vel = np.array([
        [2.92, -7.77,  8.49],
        [2.92,  2.08,  3.91],
        [2.92,  1.19, -1.84],
        [2.92,  2.17, -7.14]
    ])
    # Test entire data structure
    np.testing.assert_allclose(earth_sample.jd, expected_jd, atol=1e-6)
    assert earth_sample.date == expected_date
    np.testing.assert_allclose(earth_sample.pos, expected_pos, atol=1e-2)
    np.testing.assert_allclose(earth_sample.vel, expected_vel, atol=1e-2)
        
def test_parse_horizons_vectors():
    # Tests data structure from horizons csv parser
    
    script_dir = Path(__file__).resolve().parent   # orbitaltoolkit/tests/
    data_path = script_dir.parent / "docs" / "tests" / "ephem_vector_test.txt"  # ..orbitaltoolkit/docs/test/ephem_test.txt
    earth_sample = parse_horizons_vectors(data_path)
    # Print to verify visually
    print("\nVector sample:\n",earth_sample)

    # Expected/desired data and form
    expected_jd = np.array([2461236.5, 2461237.5, 2461238.5])
    expected_date = ['2026-Jul-15', '2026-Jul-16', '2026-Jul-17']
    expected_pos = np.array(
        [(57160730.70876996, -141598120.7516536, 23589.56327623129), 
         (59495871.96567523, -140615148.7133264, 23590.56279866397), 
         (61813980.9131555,  -139592581.9428777, 23595.60198458284)]
    )
    expected_vel = np.array(
        [(27.12293436419436, 11.14660305110507, -3.570136883634945e-05), 
         (26.92988616042405, 11.60676394181251,  4.6961136821011e-05), 
         (26.72870944821564, 12.06310798152579,  5.777203487689064e-05)]
         )
    expected_name = "Earth"
    # Test entire data structure
    np.testing.assert_allclose(earth_sample.jd, expected_jd, atol=1e-6)
    assert earth_sample.date == expected_date
    np.testing.assert_allclose(earth_sample.pos, expected_pos, atol=1e-2)
    np.testing.assert_allclose(earth_sample.vel, expected_vel, atol=1e-2)
    assert earth_sample.name == expected_name

def test_create_ephemeris_from_pos_vel():
    # Tests creation of Ephemeris dataclass from position and velocity arrays
    pos = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    vel = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]])
    name = "Test Body"
    start_jd = 2451545.0
    step_size = 1.0
    start_date = "2000-Jan-01"

    ephem = create_ephemeris_from_pos_vel(pos, vel, name=name, start_jd=start_jd, step_size=step_size, start_date=start_date)

    expected_jd = np.array([2451545.0, 2451546.0, 2451547.0])
    expected_date = ["2000-Jan-01", "2000-Jan-01", "2000-Jan-01"]

    np.testing.assert_allclose(ephem.jd, expected_jd)
    assert ephem.date == expected_date
    np.testing.assert_allclose(ephem.pos, pos)
    np.testing.assert_allclose(ephem.vel, vel)
    assert ephem.name == name


if __name__ == '__main__': 
    test_parse_horizons_csv()
    test_parse_horizons_vectors()
    test_create_ephemeris_from_pos_vel()