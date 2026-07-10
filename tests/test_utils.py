### test_utils.py
# Created 7/10/2026
# Author: Quaid Garton
# Last updated 7/10/2026

# Tests utils.py
### Current tests
# test_parse_horizons_csv()
from pathlib import Path
from orbitkit.utils import parse_horizons_csv
import numpy as np

def test_parse_horizons_csv():
    # Tests data structure from horizons csv parser
    
    script_dir = Path(__file__).resolve().parent   # orbitaltoolkit/tests/
    data_path = script_dir.parent / "docs" / "tests" / "ephem_test.txt"  # ..orbitaltoolkit/docs/test/ephem_test.txt
    earth_sample = parse_horizons_csv(data_path)
    print(earth_sample)

    # Expected/desired data and form
    expected_jd = np.array([41.5, 43.5, 45.5, 47.5])
    expected_dates = ['A.D. 2005-Jun-20', 'A.D. 2005-Jun-22',
                       'A.D. 2005-Jun-24', 'A.D. 2005-Jun-26']
    expected_states = np.array([
        [-3.42, -1.51,  2.15,  2.92, -7.77,  8.49],
        [ 1.63, -1.52,  2.26,  2.92,  2.08,  3.91],
        [ 6.69, -1.51,  2.28,  2.92,  1.19, -1.84],
        [ 1.17, -1.51,  2.2 ,  2.92,  2.17, -7.14],
    ])

    if __name__ != '__main__':
        # Test entire data structure
        np.testing.assert_allclose(earth_sample.jd, expected_jd, atol=1e-6)
        assert earth_sample.dates == expected_dates
        np.testing.assert_allclose(earth_sample.states, expected_states, atol=1e-2)


if __name__ == '__main__': 
    test_parse_horizons_csv()