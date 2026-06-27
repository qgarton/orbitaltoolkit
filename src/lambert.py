### lambert.py
# Created 6/2/2026
# Author Quaid Garton
# Last updated 6/2/2026

# Solves Lamberts problem to calculate a transfer orbit between two points

import time
import math
import numpy as np
import os
import sys
import subprocess
from scipy.optimize import fsolve

from test import test



def lambertEq(TOF, c, s, mu, dtheta):
    amin = s / 2
    n = math.sqrt(mu / amin**3)
    alpha = 2 * math.asin(math.sqrt(s / (2 * amin)))
    beta = 2 * math.asin(math.sqrt((s - c) / (2 * amin)))

    TOFmin = 1 / n * ((alpha - beta) - (math.sin(alpha) - math.sin(beta)))

    if dtheta < math.pi:
        if TOF < TOFmin:
            def f(x):
                return (1 / math.sqrt(mu / x**3) * ((2 * math.asin(math.sqrt(s / (2 * x))) - 2 * math.asin(math.sqrt((s - c) / (2 * x)))) - 
                        (math.sin(2 * math.asin(math.sqrt(s / (2 * x)))) - math.sin(2 * math.asin(math.sqrt((s - c) / (2 * x))))))) - TOF
            Scenario = 1
        else:
            def f(x):
                return (1 / math.sqrt(mu / x**3) * ((2 * math.pi - 2 * math.asin(math.sqrt(s / (2 * x))) - 2 * math.asin(math.sqrt((s - c) / (2 * x)))) - 
                        (math.sin(2 * math.pi - 2 * math.asin(math.sqrt(s / (2 * x)))) - math.sin(2 * math.asin(math.sqrt((s - c) / (2 * x))))))) - TOF
            Scenario = 2
    else:
        if TOF < TOFmin:
            def f(x):
                return (1 / math.sqrt(mu / x**3) * ((2 * math.asin(math.sqrt(s / (2 * x))) - -2 * math.asin(math.sqrt((s - c) / (2 * x)))) - 
                        (math.sin(2 * math.asin(math.sqrt(s / (2 * x)))) - math.sin(-2 * math.asin(math.sqrt((s - c) / (2 * x))))))) - TOF
            Scenario = 3
        else:
            def f(x):
                return (1 / math.sqrt(mu / x**3) * ((2 * math.pi - 2 * math.asin(math.sqrt(s / (2 * x))) - -2 * math.asin(math.sqrt((s - c) / (2 * x)))) - 
                        (math.sin(2 * math.pi - 2 * math.asin(math.sqrt(s / (2 * x)))) - math.sin(-2 * math.asin(math.sqrt((s - c) / (2 * x))))))) - TOF
            Scenario = 4

    a = fsolve(f, amin)[0]
    # print("acalc =",a)
    return a, Scenario


def lambert(initialState, finalState, TOF, mu):
    # Given initial and final position/velocity, TOF, and gravitational
    # parameter, calculates required deltaV to go between to states
    r1 = np.array(initialState[0:3])  # [km]
    R1 = np.linalg.norm(r1)
    v1 = np.array(initialState[3:6])
    V1 = np.linalg.norm(v1)
    r2 = np.array(finalState[0:3])  # [km]
    R2 = np.linalg.norm(r2)
    v2 = np.array(finalState[3:6])
    V2 = np.linalg.norm(v2)

    dtheta = np.arccos(np.dot(r1, r2) / (R1 * R2))
    if dtheta > np.pi:
        dtheta = 2 * np.pi - dtheta

    c = np.sqrt(R1**2 + R2**2 - 2 * R1 * R2 * np.cos(dtheta))
    s = (R1 + R2 + c) / 2
    a, Scenario = lambertEq(TOF, c, s, mu, dtheta)

    n = np.sqrt(mu / a**3)
    alpha = 2 * np.arcsin(np.sqrt(s / (2 * a)))
    beta = 2 * np.arcsin(np.sqrt((s - c) / (2 * a)))

    if Scenario == 1:
        pass
    elif Scenario == 2:
        alpha = 2 * np.pi - alpha
    elif Scenario == 3:
        beta = -beta
    elif Scenario == 4:
        alpha = 2 * np.pi - alpha
        beta = -beta

    TOFCHECK = TOF - 1 / n * ((alpha - beta) - (np.sin(alpha) - np.sin(beta)))

    p = 4 * a * (s - R1) * (s - R2) / c**2 * (np.sin((alpha + beta) / 2))**2
    e = np.sqrt(1 - p / a)

    def acosd(x):
        return np.degrees(np.arccos(x))

    def sind(x):
        return np.sin(np.radians(x))

    def cosd(x):
        return np.cos(np.radians(x))

    thetapossible1 = [acosd((p / R1 - 1) / e), -acosd((p / R1 - 1) / e)]
    thetapossible2 = [acosd((p / R2 - 1) / e), -acosd((p / R2 - 1) / e)]
    dthetadeg = np.degrees(dtheta)
    dthetaTol = [dthetadeg - 1e-5, dthetadeg + 1e-4]

    theta1 = None
    theta2 = None
    for i in range(2):
        for j in range(2):
            diff = thetapossible2[j] - thetapossible1[i]
            if (dthetaTol[0] < diff < dthetaTol[1] or
                dthetaTol[0] < diff + 360 < dthetaTol[1] or
                dthetaTol[0] < diff - 360 < dthetaTol[1]):
                theta1 = thetapossible1[i]
                theta2 = thetapossible2[j]

    h = np.sqrt(mu * p)
    r1pqr = np.array([R1 * cosd(theta1), R1 * sind(theta1), 0])
    r2pqr = np.array([R2 * cosd(theta2), R2 * sind(theta2), 0])

    vr1 = mu / h * e * sind(theta1)
    vt1 = mu / h * (1 + e * cosd(theta1))
    v1pqr = np.array([
        vr1 * cosd(theta1) - vt1 * sind(theta1),
        vr1 * sind(theta1) + vt1 * cosd(theta1),
        0
    ])

    vr2 = mu / h * e * sind(theta2)
    vt2 = mu / h * (1 + e * cosd(theta2))
    v2pqr = np.array([
        vr2 * cosd(theta2) - vt2 * sind(theta2),
        vr2 * sind(theta2) + vt2 * cosd(theta2),
        0
    ])

    # f and g functions to convert to
    f = (r2pqr[0] * v1pqr[1] - r2pqr[1] * v1pqr[0]) / h
    g = (r1pqr[0] * r2pqr[1] - r1pqr[1] * r2pqr[0]) / h
    fdot = (v2pqr[0] * v1pqr[1] - v2pqr[1] * v1pqr[0]) / h
    gdot = (r1pqr[0] * v2pqr[1] - r1pqr[1] * v2pqr[0]) / h

    v1XYZ = (r2 - f * r1) / g
    v2XYZ = fdot * r1 + gdot * v1XYZ

    dv1 = np.linalg.norm(v1XYZ - v1)
    dv2 = np.linalg.norm(v2 - v2XYZ)
    dV = dv1 + dv2

    return dv1, dv2


def lambertsProblem(initialState, finalState, TOF, mu):
# Given initial and final position/velocity, TOF, and gravitational parameter, 
# calculates required deltaV to go between two states
    r1 = initialState[0:2] #[km]
    R1 = np.linalg.norm(r1)
    v1 = initialState[3:5] #[km/s]
    V1 = np.linalg.norm(v1)
    r2 = finalState[0:2] #[km]
    R2 = np.linalg.norm(r2)
    v2 = finalState[3:5] #[km/s]
    V2 = np.linalg.norm(v2) 
    
    
    
    
    
    
    
    (dv1, dv2) = lambert(initialState, finalState, TOF, mu) # ["\nstill", "nothin"]
    return [dv1, dv2]

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
