### test_lambert.py
# Created 6/27/2026
# Author Quaid Garton
# Last updated 6/27/2026

# tests the lambert.py function using previous HW problem from ASEN 5050 at CU Boulder
# Next will implement test compared to Hohmann transfer

import time

from lambert import lambert
from lambert import lambertsProblem
from test import test

def main():
  # Track runtime
  start_time = time.perf_counter()
  
  # args = sys.argv[1:]) # Extracts arguments after script call
  init = [.39714e8, 5.24330e7, -2.69070e3, -10.96076, 27.77178,  -674710e-4]
  fin = [-1.021116e8, 3.32397e7, 6.34862e6, -11.00778, -33.46124, 0.17587]
  TOF = (2459621.5 - 2459501.5) *24 *3600 # [seconds]
  muSun = 1.32712428e11 #[km^3/s^2]
  (dv1, dv2) = lambertsProblem(init, fin, TOF, muSun)
  print('dv1, dv2 = ',dv1,dv2)
  
  testnum = 3
  number = test(testnum)
  #print('we changed', testnum, 'to', number)

  # Calc and print execution time
  end_time = time.perf_counter()
  execution_time = end_time - start_time
  print(f"Execution time: {execution_time:.6f} seconds")

if __name__ == '__main__':
  main()