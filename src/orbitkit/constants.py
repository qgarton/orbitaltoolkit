### constants.py
# Created 7/15/2026
# Author: Quaid Garton
# Last updated: 7/15/2026

# Branched from utils.py
# Defines certain useful constants and celestial body parameters

G = 6.67408e-11 * 1e-9  # [km^3/(kg*s^2)] Gravitational constant converted from m^3 by 1e-9
AU = 149.6e6 # [km in 1 AU]

def planet_params():
    ### Celestial Body Initialization
    ## Assume:
    # All planetary orbits are circular (For SOI calc)

    ## Units:
    # mass [kg], photosphere radius [km], distance from sun [km], SOI [km]

    def make_body(name, mass, radius, dis_to_orbited_body, mass_orbited_body):
        # Returns a Dict with name, mass, mean equatorial radius, distance from orbited body, SOI, and mu
        # Input name as str, mass in kg, radius in km, and distance from sun in AU
        SOI = dis_to_orbited_body * (mass / mass_orbited_body) ** (2/5) if dis_to_orbited_body > 0 else float('nan')
        mu = G * mass
        return {'name': name, 'mass': mass, 'radius': radius, 'dis': dis_to_orbited_body, 'SOI': SOI, 'mu': mu}
   
    Sun     = make_body("Sun"    , 1.9891e30    , 6.95508e5, 0.      , 0)
    Mercury = make_body("Mercury", 3.3022e23    , 2439.7   , 0.387*AU, Sun['mass'])
    Venus   = make_body("Venus"  , 4.869e24     , 6051.8   , 0.723*AU, Sun['mass'])
    Earth   = make_body("Earth"  , 5.9722e24    , 6378.14  , 1.0 * AU, Sun['mass'])
    Moon    = make_body("Moon"   , 7.34767309e22, 1737.1   , 3.844e5 , Earth['mass'])
    Mars    = make_body("Mars"   , 6.4171e23    , 3396.2   , 1.524*AU, Sun['mass'])

    bodies = {"Sun" : Sun, "Mercury" : Mercury, "Venus" : Venus, "Earth" : Earth, "Moon" : Moon, "Mars" : Mars}
    return bodies

if __name__ == '__main__':
  print("\nconstants.py is a library module. Contains values for G, AU in km, and a fcn that returns a dict of dicts"
        "containing all relevant parameters of solar system bodies for numerical integration\n"
        "To use:\nfrom orbitkit.constants import G, AU, planet_params\norbital_bodies = planet_params()")