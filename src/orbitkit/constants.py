### constants.py
# Created 7/15/2026
# Author: Quaid Garton
# Last updated: 7/15/2026

# Branched from utils.py
# Defines certain useful constants (G, AU) and celestial body parameters (dict of dicts)

G = 6.67408e-11 * 1e-9  # [km^3/(kg*s^2)] Gravitational constant converted from m^3 by 1e-9
AU = 149.6e6 # [km in 1 AU]
muSun = 1.9891e30*G # [km^3/s^2] Gravitational parameter of the Sun, mu = G*M

def planet_params():
    ### Celestial Body Initialization

    ## Units:
    # mass [kg], photosphere radius [km], distance from sun [km], SOI [km]

    def make_body(name, mass, radius, orbited_body, pos, vel):
        """ Returns a Dict with name, mass, mean equatorial radius, name of orbited body, 
        gravitational parameter mu, and default pos/vel vectors from 2026-Jan-01
        Input name as str, mass in kg, radius in km, pos in km, and vel in km/s"""
        mu = G * mass
        return {'name': name, 'mass': mass, 'radius': radius, 
                'orbits' : orbited_body, 'mu': mu, 'pos' : pos, 'vel' : vel}
   
    bodies = {
        'Sun': make_body('Sun', 1.9891e30, 6.95508e5, 'none', 
            [-458863.96740354, -827774.24699013, 19699.67502418],
            [0.01242506, 0.00030788, -0.00023528],),
        'Mercury': make_body('Mercury', 3.3022e23, 2439.7, 'Sun',
            [-32652520.87416521, -62044362.22997473, -2030280.27755566],
            [33.31154718, -20.32288539, -4.71526222],),
        'Venus': make_body('Venus', 4.869e24, 6051.8, 'Sun',
            [12836983.3, -108801890.0, -2230859.16],
            [34.53518141, 4.15643781, -1.93508946],),
        'Earth': make_body('Earth', 5.9722e24, 6378.14, 'Sun',
            [-26531002.4, 143946900.0, 10806.8131],
            [-29.7765061, -5.39596266, 0.00017538362],),
        'Moon': make_body('Moon', 7.34767309e22, 1737.1, 'Earth',
            [-26386676.7, 144276295.0, 42559.7895],
            [-30.7808202, -4.97509745, 0.00576059492],),
        'Mars': make_body('Mars', 6.4171e23, 3396.2, 'Sun',
            [50491130.5, -208320322.0, -5577837.78],
            [24.45957742, 7.86147374, -0.43497874],),
        'Jupiter': make_body('Jupiter', 1.89813e27, 71492, 'Sun',
            [-253878209.0, 736522532.0, 2626625.18],
            [-12.50761634, -3.63998664, 0.2949114],),
        'Saturn': make_body('Saturn', 5.683e26, 60268, 'Sun',
            [1421819200.0, 37729437.3, -57266662.9],
            [-0.78986517, 9.63422122, -0.13553349],),
        'Uranus': make_body('Uranus', 8.681e25, 25559, 'Sun',
            [1477614610.0, 2512418270.0, -9811818.42],
            [-5.92036548, 3.13495703, 0.0885724],),
        'Neptune': make_body('Neptune', 1.02409e26, 24764, 'Sun',
            [4468347030.0, 76804297.0, -104559308.0],
            [-0.12946043, 5.46595528, -0.11006076],),
        'Pluto': make_body('Pluto', 1.309e22, 1188.3, 'Sun',
            [2875995750.0, -4436760750.0, -357147192.0],
            [4.72460886, 1.76615139, -1.54157477],)}
    
    return bodies

if __name__ == '__main__':
  print("\nconstants.py is a library module. Contains values for G, AU in km, and a fcn that returns a dict of dicts"
        "containing all relevant parameters of solar system bodies for numerical integration\n"
        "To use:\nfrom orbitkit.constants import G, AU, planet_params\norbital_bodies = planet_params()")