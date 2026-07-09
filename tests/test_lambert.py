### test_lambert.py
# Created 6/27/2026
# Author Quaid Garton
# Last updated 7/6/2026

# tests the lambert.py function using previous HW problem from ASEN 5050 at CU Boulder
# Next will implement test compared to Hohmann transfer

import time
# import main function lambert() from lambert.py
from orbitkit.lambert import lambert

### Test Lambert function with known values
def test_lambert(): # Basic <180° transfer angle
  # ============================================================
  # TEST 1 — Earth to Venus (heliocentric, km/s)
  ## Source: From ASEN 5050 HW6 problem 1, CU Boulder, Fall 2021
  # Comparable to previously hand calculated values for debugging and verification of the lambert() function
  # ============================================================
  initial_state = [1.39714e8, 5.24330e7, -2.69070e3, -10.96076, 27.77178,  -6.74710e-4]
  final_state = [-1.021116e8, 3.32397e7, 6.34862e6, -11.00778, -33.46124, 0.17587]
  time_of_flight = (2459621.5 - 2459501.5) *24 *3600 # [seconds]
  muSun = 1.32712428e11 #[km^3/s^2]
  (state1_transfer, state2_transfer, dv1_1, dv2_1, dV) = lambert(initial_state, final_state, time_of_flight, muSun)
  print('\nTest 1 — Earth to Venus (heliocentric, km/s)')
  print(f'\ndv1, dv2 = {dv1_1:.4f}, {dv2_1:.4f}')
  print('Should be  3.8934, 5.1598')

  if __name__ != '__main__':
    assert abs(dv1_1 - 3.8934) < 0.1
    assert abs(dv2_1 - 5.1598) < 0.1

def test_lambert_edge_case2(): # Basic <180° transfer angle
  # ============================================================
  # TEST 2 — Curtis-geometry, Earth-centered, short-way (<180°) transfer
  ## Source: Example 5.2 from: Curtis, H. D. (2020 or later edition). 
  ## Orbital Mechanics for Engineering Students (4th ed.). Butterworth-Heinemann/Elsevier.
  # Expected dv values from norm of Curtis velocity vectors
  # ============================================================
  initial_state = [5000, 10000, 2100, 0,0,0] # -4.99249464, 1.92536342, 3.24563653] # AI generated to make dv=1.0
  final_state   = [-14600, 2500, 7000, 0,0,0] # -3.31246031, -6.19661731, -0.38528762] # AI generated to make dv=2.0
  time_of_flight = 3600.0
  mu_earth = 398600.0
  (state1_transfer, state2_transfer, dv1_2, dv2_2, dV) = lambert(initial_state, final_state, time_of_flight, mu_earth)
  print('\nTest 2 — Curtis-geometry, Earth-centered, short-way (<180°) transfer')
  print(f'\ndv1, dv2 = {dv1_2:.4f}, {dv2_2:.4f}')
  print(f'Should be  7.0817, 5.3603')
  if __name__ != '__main__':
    assert abs(dv1_2 - 7.0817) < 0.1
    assert abs(dv2_2 - 5.3603) < 0.1

def test_lambert_edge_case3(): # Test >180° transfer angle
  # ============================================================
  # TEST 3 — Earth-centered, LONG-WAY (>180°) transfer angle
  ## Source: AI generated, to be replaced when I have a working propagator to generate a real long-way transfer.
  # Zero-maneuver edge case: initial/final velocities ARE the natural transfer
  # velocities, so a correct solver must return ~0. Great for catching
  # short-way/long-way branch-selection bugs.
  # ============================================================
  initial_state = [13341.36970064, 4855.86145537, 0.0, -1.60060673, 5.80158914, 0.0]
  final_state   = [-6936.4926741, -19057.8569923, 0.0, 4.39763084, -0.19664843, 0.0]
  time_of_flight = 21433.248160924064
  mu_earth = 398600.0
  (state1_transfer, state2_transfer, dv1_3, dv2_3, dV) = lambert(initial_state, final_state, time_of_flight, mu_earth)
  print('\nTest 3 — Earth-centered, LONG-WAY (>180°) transfer angle')
  print(f'\ndv1, dv2 = {dv1_3:.4f}, {dv2_3:.4f}')
  print('Should be  0, 0')
  # (transfer angle here is 230°, i.e. genuinely past the half-revolution mark)
  if __name__ != '__main__':
    assert abs(dv1_3 - 0.0) < 0.1
    assert abs(dv2_3 - 0.0) < 0.1

def test_lambert_edge_case4(): # Test unit hardcodes
  # ============================================================
  # TEST 4 — Battin-geometry, AU/year units (not km/s!)
  ## Source: Problem 7-12 from Battin, R. H. An Introduction to the Mathematics 
  ## and Methods of Astrodynamics, Revised Edition. AIAA Education Series.
  # Great for catching bugs where AU instead of km scale could cause issues 
  # (e.g. hardcoded epsilon/tolerance values that only work at km magnitudes)
  # Expected dv values from norm of Battin velocity vectors, in AU/year units
  # ============================================================
  initial_state = [0.159321004, 0.579266185, 0.052359607, 0,0,0] # -9.203608, 3.01862016, 1.53636008] # AI generated to make dv=0.1
  final_state   = [0.057594337, 0.605750797, 0.068345246, 0,0,0] # -9.511186, 1.83884006, 1.42137810] # AI generated to make dv=0.05
  time_of_flight = 0.010794065
  mu_sun_au = 39.47692641
  v1_transfer = [-9.303608, 3.01862016, 1.53636008] #AU/yr
  v2_transfer = [-9.511186, 1.88884006, 1.42137810] #AU/yr
  (state1_transfer, state2_transfer, dv1_4, dv2_4, dV) = lambert(initial_state, final_state, time_of_flight, mu_sun_au)
  print('\nTest 4 — Battin-geometry, AU/year units (not km/s!)')
  print(f'\ndv1, dv2 = {dv1_4:.4f}, {dv2_4:.4f}')
  print(f'Should be  9.9010, 9.8005')

  if __name__ != '__main__':
    assert abs(dv1_4 - 9.9010) < 0.1
    assert abs(dv2_4 - 9.8005) < 0.1


if __name__ == '__main__':
  # Track runtime
  start_time = time.perf_counter()
  test_lambert()
  test_lambert_edge_case2()
  test_lambert_edge_case3()
  test_lambert_edge_case4()
  # Calc and print execution time
  end_time = time.perf_counter()
  execution_time = end_time - start_time
  print(f"Execution time: {execution_time:.6f} seconds\n")