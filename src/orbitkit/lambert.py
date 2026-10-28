### lambert.py
# Created 6/2/2026
# Author Quaid Garton
# Last updated 7/7/2026

#### FUTURE EDITS:
### Change inputs to (r1,r2,TOF,mu) and outputs to v1,v2,(relative_tol?), Create new dV Calc fcn or do it outside of here
### Make mu=muSun a default var, maybe from constants.py

# Uses Lamberts theorem to solve Lamberts problem to calculate a transfer orbit between two points given a time of flight
## Assumptions: 
# Less than one revolution along an elliptical orbit, two body orbit, no significant perturbations, impulse burns

import numpy as np 
from scipy.optimize import fsolve


def norm(vec):
    return np.linalg.norm(vec)

def transfer_angle(r1, r2, prograde=True):
    """Calculates the transfer angle in radians between two position vectors r1 and r2."""
    R1 = np.linalg.norm(r1)
    R2 = np.linalg.norm(r2)
    ratio = np.clip(np.dot(r1, r2) / (R1 * R2), -1, 1) # Clip to valid range in case of numerical errors (e.g., due to floating-point precision)
    dtheta = np.arccos(ratio)
    cross_z = np.cross(r1, r2)[2] # z-hat cross product value to determine direction
    if prograde: 
        if cross_z < 0: # [rad] if the cross product of the two position vectors is negative, the transfer angle is greater than 180 degrees
            dtheta = 2*np.pi - dtheta
    else:
        if cross_z >= 0:
            dtheta = 2*np.pi - dtheta
    return dtheta

def lambertEq(TOF, c, s, mu, dtheta):
    ## Calculates the semi-major axis of the transfer orbit given the time of flight, 
    # chord length, semi-perimeter, gravitational parameter, and change in true anomaly
    amin = s / 2 # [km] minimum semi-major axis of the transfer orbit
    nmin = np.sqrt(mu / amin**3) # [rad/s] mean motion of minimum semi-major axis transfer orbit
    alpha_min = 2 * np.arcsin(np.sqrt(s / (2 * amin)))
    beta_min = 2 * np.arcsin(np.sqrt((s - c) / (2 * amin)))

    TOFmin = 1 / nmin * ((alpha_min - beta_min) - (np.sin(alpha_min) - np.sin(beta_min))) # [s] minimum time of flight for the transfer orbit

    if dtheta < np.pi:
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


def lambert(r1, r2, TOF, mu):
    ## Calculates the required velocity of the transfer arc to go between two states given 
    # initial and final position, time of flight, and gravitational parameter
    r1 = np.array(r1)
    r2 = np.array(r2)
    R1 = np.linalg.norm(r1) # [km] magnitude of initial position vector
    R2 = np.linalg.norm(r2) # [km] magnitude of final position vector

    dtheta = transfer_angle(r1, r2, prograde=True) # [rad] change in true anomaly

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

    ## Ensure that the time of flight check is within a reasonable relative tolerance
    TOFCHECK = TOF - 1 / n * ((alpha - beta) - (np.sin(alpha) - np.sin(beta)))
    relative_tol = abs(TOFCHECK)/TOF - 1
    if relative_tol > 1e-6:
        print("Warning: Time of flight check failed.\n   TOF = ", TOF, "\n   Relative Error = ", relative_tol, "\n   TOF error (s) = ", TOF)

    ### Avoids theta ~= 180 since g function is calculated incorrectly there
    DTHETA_TOL = np.radians(.9) # barely <2e-2 radians
    if dtheta < DTHETA_TOL or abs(np.pi - dtheta) < DTHETA_TOL:
        raise ValueError(
            f"Transfer angle too close to 0 or 180 deg (dtheta={np.degrees(dtheta):.6f} deg); "
            "orbital plane is degenerate/ill-conditioned for this r1, r2 pair."
        )

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

    return v1_transfer_XYZ, v2_transfer_XYZ, relative_tol

if __name__ == '__main__':
  print("\nlambert.py is a library module. Run 'python3 test_lambert.py' to test.\n" \
    "Or call lambert.lambert(InitialState, FinalState, TimeOfFlight, GravitationalParameter)"\
    " from another script to use the function.\n")
    
