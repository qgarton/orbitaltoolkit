### test_lambert.py
# Created 6/27/2026
# Author Quaid Garton
# Last updated 7/6/2026

# tests the lambert.py function using previous HW problem from ASEN 5050 at CU Boulder
# Next will implement test compared to Hohmann transfer

import time
# import main function lambert() from lambert.py
from orbitkit.lambert import lambert


def test_lambert():
  # Track runtime
  start_time = time.perf_counter()
  
  ## Test Lambert function with known values
  initial_state = [.39714e8, 5.24330e7, -2.69070e3, -10.96076, 27.77178,  -674710e-4]
  final_state = [-1.021116e8, 3.32397e7, 6.34862e6, -11.00778, -33.46124, 0.17587]
  time_of_flight = (2459621.5 - 2459501.5) *24 *3600 # [seconds]
  muSun = 1.32712428e11 #[km^3/s^2]
  (state1_transfer, state2_transfer, dv1, dv2, dV) = lambert(initial_state, final_state, time_of_flight, muSun)
  print(f'\ndv1, dv2 = {dv1:.4f}, {dv2:.4f}')
  print('Should be  73.0720, 22.4514')

  # Calc and print execution time
  end_time = time.perf_counter()
  execution_time = end_time - start_time
  print(f"Execution time: {execution_time:.6f} seconds\n")
  if __name__ != '__main__':
    assert abs(dv1 - 73.0720) < 0.1
    assert abs(dv2 - 22.4514) < 0.1

if __name__ == '__main__':
  test_lambert()