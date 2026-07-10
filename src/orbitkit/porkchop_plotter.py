### porkchop_plotter.py
# Created 7/9/2026
# Author: Quaid Garton
# Last updated: 7/9/2026

# Creates a porkchop plot for a given set of initial and final states, time of flight, and gravitational parameter

import numpy as np
import time
import matplotlib.pyplot as plt

def porkchop_plotter(initial, final, mu, lambert_fn):
    # Run through all variations of time/position data of Earth and Mars
    start = time.time()
    index = []
    for i in range(len(initial.jd)):
        for j in range(len(final.jd)):
            if initial.jd[i] < final.jd[j]:
                index.append((i, j))
    NumRuns = len(index) + 1
    print(f"Elapsed time for indexing: {time.time() - start:.2f} seconds")

    # Calculate matrix of each deltaV
    start = time.time()
    count = 0
    dV1 = np.zeros((len(final.jd), len(initial.jd)))
    dV2 = np.zeros((len(final.jd), len(initial.jd)))

##### Error is with the initial.states[i,:], need to look at ephemeris data structure when called
    for j in range(len(final.jd)):
        for i in range(len(initial.jd)):
            if initial.jd[i] < final.jd[j]:
                TOF = (final.jd[j] - initial.jd[i]) * 24 * 3600
                _, _, dV1[j, i], dV2[j, i], _ = lambert_fn(initial.states[i, :], final.states[j, :], TOF, mu)
                count += 1
                if count % 100 == 0:
                    print(f"On run {count}/{NumRuns}")
            else:
                break
    print(f"Elapsed time for deltaV calculation: {time.time() - start:.2f} seconds")

    start_time = time.time()
    plt.figure()
    cp = plt.contour(initial.jd - initial.jd[0], final.jd - initial.jd[0], dV1, levels=200)
    plt.clabel(cp, inline=True, fontsize=10, fmt='%1.1f') # labels contours
    plt.xlabel("Earth Departure date (June 20 - Sep 20 2005)")
    plt.ylabel("Mars Arrival date (Dec 1 - June 19 2005/6)")
    plt.title(r"$\Delta V$ Required Upon Departure [Day 0 = June 20]")
    plt.colorbar()
    '''
    x_labels = Edate[::10]                  # String values at those positions
    plt.xticks(ticks=Etime - Etime[0], labels=x_labels, rotation=45)
    y_labels = Mdate[::10]                  # String values at those positions
    plt.yticks(ticks=Mtime - Etime[0], labels=y_labels, rotation=45) 
    '''
    plt.figure()
    cp = plt.contour(initial.dates, final.dates, dV1, levels=200)
    plt.clabel(cp, inline=True, fontsize=10, fmt='%1.1f') # labels contours
    plt.xlabel("Earth Departure date (June 20 - Sep 20 2005)")
    plt.ylabel("Mars Arrival date (Dec 1 - June 19 2005/6)")
    plt.title(r"$\Delta V$ Required Upon Departure [Day 0 = June 20]")
    plt.colorbar()
    ''''''
    # Label X-axis with every 10th string from Edate (Makes us lose ability to hover over data)
    x_ticks = initial.jd[::10] - initial.jd[0]              # Numeric positions: 0, 10, 20...
    x_labels = initial.dates[::10]                  # String values at those positions
    plt.xticks(ticks=x_labels, labels=x_labels, rotation=45)

    # Label Y-axis with every 10th string from Mdate
    y_ticks = final.jd[::10] - initial.jd[0]             # Numeric positions: 0, 10, 20...
    y_labels = final.dates[::10]                  # String values at those positions
    plt.yticks(ticks=y_labels, labels=y_labels, rotation=45) 

    plt.tight_layout() # Ensures labels don't get cut off at bottom/sides
    #'''
    ''''''
    plt.figure()
    cp = plt.contour(initial.jd - initial.jd[0], final.jd - initial.jd[0], dV2, levels=200)
    plt.clabel(cp, inline=True, fontsize=10, fmt='%1.1f') # labels contours
    plt.xlabel("Earth Departure date (June 20 - Sep 20 2005)")
    plt.ylabel("Mars Arrival date (Dec 1 - June 19 2005/6)")
    plt.title(r"$\Delta V$ Required Upon Arrival [Day 0 = June 20]")
    plt.colorbar()

    # Uncomment below to plot total delta V required
    plt.figure()
    cp = plt.contour(initial.jd - initial.jd[0], final.jd - initial.jd[0], dV1 + dV2, levels=200)
    plt.clabel(cp, inline=True, fontsize=10, fmt='%1.1f') # labels contours
    plt.xlabel("Earth Departure date (June 20 - Sep 20 2005)")
    plt.ylabel("Mars Arrival date (Dec 1 - June 19 2005/6)")
    plt.title(r"Total $\Delta V$ Required [Day 0 = June 20]")
    plt.colorbar()
    # breakpoint()
    # '''
    plt.show()
    print(f"Elapsed time: {time.time() - start_time:.2f} seconds")
