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

    TOL = 1e-6
    for j in range(len(final.jd)):
        for i in range(len(initial.jd)):
            if initial.jd[i] < final.jd[j]:
                TOF = (final.jd[j] - initial.jd[i]) * 24 * 3600
                try:
                    v1_transfer, v2_transfer, relative_tol = lambert_fn(initial.pos[i, :], final.pos[j, :], TOF, mu)
                    ## Avoids incorrectly calculated dVs
                    if relative_tol > TOL:
                        dV1[j, i] = np.nan
                        dV2[j, i] = np.nan
                        print("Nan value Assigned")
                    else:
                        dV1[j, i] = np.linalg.norm(v1_transfer - initial.vel[i,:])
                        dV2[j, i] = np.linalg.norm(final.vel[j,:] - v2_transfer)
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

def plot_porkchops(initial, final, dV1, dV2, plot="subplot"):
    levels = np.linspace(0, 30, 20)
    if not initial.name: initial.name = "Initial Body"
    if not final.name: final.name = "Final Body"

    # Find min dV and index for occurrence
    dV_tot = dV1 + dV2
    j_min, i_min = np.unravel_index(np.nanargmin(dV_tot), dV_tot.shape)
    min_dV = dV_tot[j_min, i_min]
    departure_date = initial.date[i_min]
    arrival_date = final.date[j_min]

    datasets = [dV1, dV2, dV_tot]
    titles = [
        r"$\Delta V$ Upon Departure",
        r"$\Delta V$ Upon Arrival",
        r"Total $\Delta V$",
    ]

    # Sub plotter
    if plot == "subplot":
        fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
        for ax, data, title in zip(axes, datasets, titles):
            cp = ax.contour(initial.jd - initial.jd[0], final.jd - initial.jd[0], data, levels=levels)
            ax.clabel(cp, inline=True, fontsize=8, fmt='%1.1f')
            ax.set_xlabel(f"{initial.name} Departure date ({initial.date[0]} - {initial.date[-1]})")
            ax.set_ylabel(f"{final.name} Arrival date ({final.date[0]} - {final.date[-1]})")
            ax.set_title(title, fontsize=11)
            fig.colorbar(cp, ax=ax, pad=0.02)
        
        fig.suptitle(
            rf"{initial.name}$\to${final.name} Transfer $\Delta V$  [Day 0 = {initial.date[0]}]" f"\n" 
            rf"Min Total $\Delta V$ = {min_dV:.4f} km/s    |    on {departure_date}$\to${arrival_date}    |    "
            rf"TOF of {final.jd[j_min] - initial.jd[i_min]} days",fontsize=13)
        plt.tight_layout(rect=[0, 0, 1, 0.93])  # leave room at top for suptitle
    
    # 3 Full plots
    elif plot == "fullplot":
        for data, title in zip(datasets, titles):
            plt.figure()
            cp = plt.contour(initial.jd - initial.jd[0], final.jd - initial.jd[0], data, levels=levels)
            plt.clabel(cp, inline=True, fontsize=10, fmt='%1.1f') # labels contours
            plt.xlabel(f"{initial.name} Departure date ({initial.date[0]} - {initial.date[-1]})")
            plt.ylabel(f"{final.name} Arrival date ({final.date[0]} - {final.date[-1]})")
            plt.title(rf"{title} [Day 0 = {initial.date[0]}]")
            plt.colorbar()
    
    else:
        raise ValueError(f"plot must be 'subplot' or 'fullplot', got {plot!r}")

    plt.show()
