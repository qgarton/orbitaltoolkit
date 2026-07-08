### lambert.py
# Created 6/2/2026
# Author Quaid Garton
# Last updated 7/7/2026

# Solves Lamberts problem to calculate a transfer orbit between two points given a time of flight
## Assumptions: 
# Less than one half revolution along an elliptical orbit, two body orbit, no significant perturbations, impulse burns

import numpy as np 
from scipy.optimize import fsolve


def lambertEq(TOF, c, s, mu, dtheta):
    ## Calculates the semi-major axis of the transfer orbit given the time of flight, 
    # chord length, semi-perimeter, gravitational parameter, and change in true anomaly
    amin = s / 2 # [km] minimum semi-major axis of the transfer orbit
    nmin = np.sqrt(mu / amin**3) # [rad/s] mean motion of minimum semi-major axis transfer orbit
    alpha_min = 2 * np.arcsin(np.sqrt(s / (2 * amin)))
    beta_min = 2 * np.arcsin(np.sqrt((s - c) / (2 * amin)))

    TOFmin = 1 / nmin * ((alpha_min - beta_min) - (np.sin(alpha_min) - np.sin(beta_min))) # [s] minimum time of flight for the transfer orbit

    if dtheta < np.pi: #### Currently always true since we are using the shorter path, but could be changed in the future
        if TOF < TOFmin:
            def f(x):
                return (1 / np.sqrt(mu / x**3) * ((2 * np.arcsin(np.sqrt(s / (2 * x))) - 2 * np.arcsin(np.sqrt((s - c) / (2 * x)))) - 
                        (np.sin(2 * np.arcsin(np.sqrt(s / (2 * x)))) - np.sin(2 * np.arcsin(np.sqrt((s - c) / (2 * x))))))) - TOF
            Scenario = 1
        else:
            def f(x):
                return (1 / np.sqrt(mu / x**3) * ((2 * np.pi - 2 * np.arcsin(np.sqrt(s / (2 * x))) - 2 * np.arcsin(np.sqrt((s - c) / (2 * x)))) - 
                        (np.sin(2 * np.pi - 2 * np.arcsin(np.sqrt(s / (2 * x)))) - np.sin(2 * np.arcsin(np.sqrt((s - c) / (2 * x))))))) - TOF
            Scenario = 2
    else:
        if TOF < TOFmin:
            def f(x):
                return (1 / np.sqrt(mu / x**3) * ((2 * np.arcsin(np.sqrt(s / (2 * x))) - -2 * np.arcsin(np.sqrt((s - c) / (2 * x)))) - 
                        (np.sin(2 * np.arcsin(np.sqrt(s / (2 * x)))) - np.sin(-2 * np.arcsin(np.sqrt((s - c) / (2 * x))))))) - TOF
            Scenario = 3
        else:
            def f(x):
                return (1 / np.sqrt(mu / x**3) * ((2 * np.pi - 2 * np.arcsin(np.sqrt(s / (2 * x))) - -2 * np.arcsin(np.sqrt((s - c) / (2 * x)))) - 
                        (np.sin(2 * np.pi - 2 * np.arcsin(np.sqrt(s / (2 * x)))) - np.sin(-2 * np.arcsin(np.sqrt((s - c) / (2 * x))))))) - TOF
            Scenario = 4

    a = fsolve(f, amin)[0]
    return a, Scenario


def lambert(initial_state, final_state, TOF, mu):
    ## Calculates the required deltaV to go between two states given 
    # initial and final position/velocity, time of flight, and gravitational parameter
    r1 = np.array(initial_state[0:3])  # [km] initial position vector
    R1 = np.linalg.norm(r1) # [km] magnitude of initial position vector
    v1 = np.array(initial_state[3:6]) # [km/s] initial velocity vector
    r2 = np.array(final_state[0:3])  # [km] final position vector
    R2 = np.linalg.norm(r2) # [km] magnitude of final position vector
    v2 = np.array(final_state[3:6]) # [km/s] final velocity vector
    
    ratio = np.dot(r1, r2) / (R1 * R2)
    ratio = np.clip(ratio, -1.0, 1.0)  # Clamp to valid range in case of numerical errors (e.g., due to floating-point precision)
    dtheta = np.arccos(ratio) # [rad] change in true anomaly
        
    #### Used for specific case where we want shorter path to be used, Might want to change eventually to allow for longer path usage
    if dtheta > np.pi: # [rad] if the change in true anomaly is greater than 180 degrees, use the shorter path
        dtheta = 2 * np.pi - dtheta
    ####

    c = np.sqrt(R1**2 + R2**2 - 2 * R1 * R2 * np.cos(dtheta)) # [km] chord length between initial and final position vectors
    s = (R1 + R2 + c) / 2 # [km] semi-perimeter of the triangle formed by the initial and final position vectors and the chord length
    a, Scenario = lambertEq(TOF, c, s, mu, dtheta) # [km] semi-major axis of the transfer orbit and scenario number

    n = np.sqrt(mu / a**3) # [rad/s] mean motion of the transfer orbit
    alpha = 2 * np.arcsin(np.sqrt(s / (2 * a))) # [rad]
    beta = 2 * np.arcsin(np.sqrt((s - c) / (2 * a))) # [rad]

    if Scenario == 1:
        pass
    elif Scenario == 2:
        alpha = 2 * np.pi - alpha
    elif Scenario == 3:
        beta = -beta
    elif Scenario == 4:
        alpha = 2 * np.pi - alpha
        beta = -beta

    ## Ensure that the time of flight check is within a reasonable tolerance
    TOFCHECK = TOF - 1 / n * ((alpha - beta) - (np.sin(alpha) - np.sin(beta)))
    if abs(TOFCHECK) > 1e-6:
        print("Warning: Time of flight check failed.\n   TOF = ", TOF, "\n   TOF Error = ", TOFCHECK, " seconds")

    p = 4 * a * (s - R1) * (s - R2) / c**2 * (np.sin((alpha + beta) / 2))**2 # [km] semi-latus rectum of the transfer orbit
    e = np.sqrt(1 - p / a) # [unitless] eccentricity of the transfer orbit
    
    ## Calculate the possible true anomalies at the initial and final positions
    thetapossible1 = [np.arccos((p / R1 - 1) / e), -np.arccos((p / R1 - 1) / e)]
    thetapossible2 = [np.arccos((p / R2 - 1) / e), -np.arccos((p / R2 - 1) / e)]
    dthetaTol = [dtheta - 1e-3, dtheta + 1e-2] # [rad] tolerance for change in true anomaly
    # Determine which combination of true anomalies corresponds to the desired change in true anomaly
    theta1 = None
    theta2 = None
    for i in range(2):
        for j in range(2):
            diff = thetapossible2[j] - thetapossible1[i]
            if (dthetaTol[0] < diff < dthetaTol[1] or
                dthetaTol[0] < diff + 2 * np.pi < dthetaTol[1] or
                dthetaTol[0] < diff - 2 * np.pi < dthetaTol[1]):
                theta1 = thetapossible1[i]
                theta2 = thetapossible2[j]

    ## Calculate r and v in perifocal frame pqw
    r1pqw = np.array([R1 * np.cos(theta1), R1 * np.sin(theta1), 0])
    r2pqw = np.array([R2 * np.cos(theta2), R2 * np.sin(theta2), 0])

    # Start with velocity in polar frame
    h = np.sqrt(mu * p) # [km^2/s] specific angular momentum of the transfer orbit
    v1_transfer_rhat = mu / h * e * np.sin(theta1) # [km/s] radial velocity in perifocal frame
    v1_transfer_that = mu / h * (1 + e * np.cos(theta1)) # [km/s] theta velocity in perifocal frame
    # Convert to perifocal frame
    v1pqw = np.array([
        v1_transfer_rhat * np.cos(theta1) - v1_transfer_that * np.sin(theta1),
        v1_transfer_rhat * np.sin(theta1) + v1_transfer_that * np.cos(theta1),
        0 ])

    # Start with velocity in polar frame
    v2_transfer_rhat = mu / h * e * np.sin(theta2) # [km/s] radial velocity in perifocal frame
    v2_transfer_that = mu / h * (1 + e * np.cos(theta2)) # [km/s] theta velocity in perifocal frame
    # Convert to perifocal frame
    v2pqw = np.array([
        v2_transfer_rhat * np.cos(theta2) - v2_transfer_that * np.sin(theta2),
        v2_transfer_rhat * np.sin(theta2) + v2_transfer_that * np.cos(theta2),
        0 ])

    ## Define f and g functions to convert to position and velocity in inertial frame XYZ
    f = (r2pqw[0] * v1pqw[1] - r2pqw[1] * v1pqw[0]) / h 
    g = (r1pqw[0] * r2pqw[1] - r1pqw[1] * r2pqw[0]) / h
    fdot = (v2pqw[0] * v1pqw[1] - v2pqw[1] * v1pqw[0]) / h
    gdot = (r1pqw[0] * v2pqw[1] - r1pqw[1] * v2pqw[0]) / h  

    # Convert velocity from perifocal frame to inertial frame
    v1_transfer_XYZ = (r2 - f * r1) / g # [km/s] transfer orbit velocity at initial position
    v2_transfer_XYZ = fdot * r1 + gdot * v1_transfer_XYZ # [km/s] transfer orbit velocity at final position

    # Calculate deltaV required for transfer and return tranfer orbit info
    state1_transfer = np.concatenate((r1, v1_transfer_XYZ))
    state2_transfer = np.concatenate((r2, v2_transfer_XYZ))
    dv1 = np.linalg.norm(v1_transfer_XYZ - v1)
    dv2 = np.linalg.norm(v2 - v2_transfer_XYZ)
    dV = dv1 + dv2

    return state1_transfer, state2_transfer, dv1, dv2, dV

if __name__ == '__main__':
  print("\nlambert.py is a library module. Run 'python3 test_lambert.py' to test.\n" \
    "Or call lambert.lambert(InitialState, FinalState, TimeOfFlight, GravitationalParameter)"\
    " from another script to use the function.\n")
    
