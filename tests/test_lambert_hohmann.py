### test_lambert_hohmann.py
# Created 7/6/2026
# Author Quaid Garton
# Last updated 7/6/2026

from numpy import sqrt, pi, set_printoptions, sin, cos, radians 

from orbitkit.lambert import lambert

### Not a true Hohmann transfer since the final position is not exactly 180 degrees from the initial position, but close enough to test the Lambert function with minimal error.
def test_lambert_hohmann():
    # Test Lambert function with calculated values for Hohmann transfer from LEO to GEO
    LEO = 7000 # [km] radius of low Earth orbit
    GEO = 42164 # [km] radius of geostationary orbit
    muEarth = 398600.4418 # [km^3/s^2] gravitational parameter of Earth
    LEO_velocity = sqrt(muEarth / LEO) # [km/s] velocity in low Earth orbit
    GEO_velocity = sqrt(muEarth / GEO) # [km/s] velocity in geostationary orbit
    initial_state = [LEO, 0, 0, 0, LEO_velocity, 0] # [km, km/s] initial position and velocity
    final_state = [GEO*cos(radians(179)), GEO*sin(radians(179)), 0, -GEO_velocity*sin(radians(179)), GEO_velocity*cos(radians(179)), 0] # [km, km/s] final position and velocity

    # Calculated transfer orbit parameters
    a_transfer = (LEO + GEO) / 2 # [km] semi-major axis of transfer orbit
    orbital_period_transfer = 2 * pi * sqrt(a_transfer**3 / muEarth) # [seconds] orbital period of transfer orbit
    time_of_flight = orbital_period_transfer/2 #* radians(179)/pi# [seconds] TOF for almost half of the transfer orbit
    velocity_transfer_perigee = sqrt(2*muEarth/LEO - muEarth/a_transfer) # [km/s] velocity at perigee of transfer orbit
    velocity_transfer_apogee = sqrt(2*muEarth/GEO - muEarth/a_transfer) # [km/s] velocity at apogee of transfer orbit
    dv1_expected = velocity_transfer_perigee - LEO_velocity # [km/s] expected deltaV at perigee
    dv2_expected = GEO_velocity - velocity_transfer_apogee # [km/s] expected

    (state1_transfer, state2_transfer, dv1, dv2, dV, _) = lambert(initial_state, final_state, time_of_flight, muEarth)
  
    # # Set print options globally to 4 significant digits
    # set_printoptions(precision=4, suppress=True)
    # print(f'\nstate1_transfer = {state1_transfer}')
    # print(f'should be.      = {LEO}, 0, 0, 0, {velocity_transfer_perigee:.4f}, 0')
    # print(f'state2_transfer = {state2_transfer}')
    # print(f'should be       = {-GEO}, 0, 0, 0, {-velocity_transfer_apogee:.4f}, 0')
    # print(f'\ndv1, dv2 = {dv1:.4f}, {dv2:.4f}')
    # print(f'Should be: {dv1_expected:.4f} km/s, {dv2_expected:.4f} km/s')


    if __name__ != '__main__':
        assert abs(dv1 - dv1_expected) < 0.1
        assert abs(dv2 - dv2_expected) < 0.1

if __name__ == '__main__':
  test_lambert_hohmann()