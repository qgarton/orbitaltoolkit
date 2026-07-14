### porkchop_plotter.py
# Created 7/9/2026
# Author: Quaid Garton
# Last updated: 7/9/2026

# Creates a porkchop plot for a given set of initial and final states, time of flight, and gravitational parameter

import numpy as np
import time
import matplotlib.pyplot as plt

def porkchop_grid_calculation(initial, final, mu, lambert_fn):
    # Run through all variations of time/position data of Earth and Mars
    index = []
    for i in range(len(initial.jd)):
        for j in range(len(final.jd)):
            if initial.jd[i] < final.jd[j]:
                index.append((i, j))
    NumRuns = len(index) + 1

    # Calculate matrix of each deltaV
    start = time.time()
    count = 0
    dV1 = np.zeros((len(final.jd), len(initial.jd)))
    dV2 = np.zeros((len(final.jd), len(initial.jd)))
    print(type(initial.states), getattr(initial.states, 'shape', 'NO SHAPE ATTR'))

    TOL = 1e-6
    for j in range(len(final.jd)):
        for i in range(len(initial.jd)):
            if initial.jd[i] < final.jd[j]:
                TOF = (final.jd[j] - initial.jd[i]) * 24 * 3600
                try:
                    _, _, dv1, dv2, _, relative_tol = lambert_fn(initial.states[i, :], final.states[j, :], TOF, mu)
                    # Avoids incorrectly calculated dVs
                    if relative_tol > TOL:
                        dV1[j, i] = np.nan
                        dV2[j, i] = np.nan
                        print("Nan value Assigned")
                    else:
                        dV1[j, i] = dv1
                        dV2[j, i] = dv2
                except Exception:
                    dV1[j, i] = np.nan
                    dV2[j, i] = np.nan

                count += 1
                if count % 200 == 0:
                    print(f"On run {count}/{NumRuns}")
            else:
                break
    print(f"Elapsed time for deltaV calculation: {time.time() - start:.2f} seconds")
    return dV1, dV2

def plot_porkchops(initial, final, dV1, dV2):
    levels = np.linspace(0, 30, 20)

    ### Fig 1 dV1
    plt.figure()
    cp = plt.contour(initial.jd - initial.jd[0], final.jd - initial.jd[0], dV1, levels=levels)
    plt.clabel(cp, inline=True, fontsize=10, fmt='%1.1f') # labels contours
    plt.xlabel("Earth Departure date (June 20 - Sep 20 2005)")
    plt.ylabel("Mars Arrival date (Dec 1 - June 19 2005/6)")
    plt.title(r"$\Delta V$ Required Upon Departure [Day 0 = June 20]")
    plt.colorbar()

    ### Fig 1 label test
    # ## Creates labels of days on axes, but is either too cluttered or looses data readability
    # plt.figure()
    # cp = plt.contour(initial.dates, final.dates, dV1, levels=levels)
    # plt.clabel(cp, inline=True, fontsize=10, fmt='%1.1f') # labels contours
    # plt.xlabel("Earth Departure date (June 20 - Sep 20 2005)")
    # plt.ylabel("Mars Arrival date (Dec 1 - June 19 2005/6)")
    # #plt.title(r"$\Delta V$ Required Upon Departure [Day 0 = June 20]")
    # plt.colorbar()
    # ## Ruins data readability but makes dates legible
    # # Label X-axis with every 10th string from Edate (Makes us lose ability to hover over data)
    # x_ticks = initial.jd[::10] - initial.jd[0]              # Numeric positions: 0, 10, 20...
    # x_labels = initial.dates[::10]                  # String values at those positions
    # plt.xticks(ticks=x_labels, labels=x_labels, rotation=45)
    # # Label Y-axis with every 10th string from Mdate
    # y_ticks = final.jd[::10] - initial.jd[0]             # Numeric positions: 0, 10, 20...
    # y_labels = final.dates[::10]                  # String values at those positions
    # plt.yticks(ticks=y_labels, labels=y_labels, rotation=45) 
    # plt.tight_layout() # Ensures labels don't get cut off at bottom/sides

    ### Fig 2 dV2
    plt.figure()
    cp = plt.contour(initial.jd - initial.jd[0], final.jd - initial.jd[0], dV2, levels=levels)
    plt.clabel(cp, inline=True, fontsize=10, fmt='%1.1f') # labels contours
    plt.xlabel("Earth Departure date (June 20 - Sep 20 2005)")
    plt.ylabel("Mars Arrival date (Dec 1 - June 19 2005/6)")
    plt.title(r"$\Delta V$ Required Upon Arrival [Day 0 = June 20]")
    plt.colorbar()

    ### Fig 3 total dV
    plt.figure()
    cp = plt.contour(initial.jd - initial.jd[0], final.jd - initial.jd[0], dV1 + dV2, levels=levels)
    plt.clabel(cp, inline=True, fontsize=10, fmt='%1.1f') # labels contours
    plt.xlabel("Earth Departure date (June 20 - Sep 20 2005)")
    plt.ylabel("Mars Arrival date (Dec 1 - June 19 2005/6)")
    plt.title(r"Total $\Delta V$ Required [Day 0 = June 20]")
    plt.colorbar()

    plt.show()
