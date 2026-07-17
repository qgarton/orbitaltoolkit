"""
### plotting.py
# Created 7/16/2026
# Author: Quaid Garton
# Last updated: 7/17/2026

Use:
plot_plotly(orbital_bodies, orbital_bodies_truth_comparison) 
# orbital_bodies[body]['prop_pos'] contains simulated position data in shape (3,n)
# orbital_bodies_truth_comparison[body].pos contains position data in shape  (n,3)
"""
# Plots position overtime of 3D integrated orbital bodies next to horizons data for the same bodies


def plot_plotly(orbital_bodies, orbital_bodies_truth_comparison=None, focus_body='Sun', zoom_radius=2.5e8, zoom_height=2e8, animate=False, frame_step=5):
    """ Plots a 3D interactive graph in your browser. Can compare/plot a secondary set of data with (some of) the same orbital bodies
    IMPORTANT: orbital_bodies[body]['prop_pos'] shape is (3,n) while orbital_bodies_truth_comparison.pos from parse_horizons_vectors() is shape (n,3)"""
    import plotly.graph_objects as go
    
    fig = go.Figure()

    for body in orbital_bodies:
        pos = orbital_bodies[body]['prop_pos']
        fig.add_trace(go.Scatter3d(
        x=pos[0], y=pos[1], z=pos[2],
        mode='lines',
        name=f'{body} path',
        ))
        fig.add_trace(go.Scatter3d(
            x=[pos[0, -1]], y=[pos[1, -1]], z=[pos[2, -1]],   # just the last point, wrapped in a list
            mode='markers',
            marker=dict(size=5),
            name=f'{body} final',
            showlegend=False,   # avoid cluttering the legend with duplicate entries
        ))
        # Plot truth comparison if available
        if orbital_bodies_truth_comparison is not None:
            if body not in orbital_bodies_truth_comparison:
                continue  # skip silently rather than crashing if truth data is missing for a body
            truth_pos = orbital_bodies_truth_comparison[body].pos  # shape (n_times, 3)
            fig.add_trace(go.Scatter3d(
            x=truth_pos[:,0], y=truth_pos[:,1], z=truth_pos[:,2],
            mode='markers', marker=dict(size=1, symbol='x'), # Make exes instead of a line
            name=f'{body} Horizons truth',
            ))
    
    ### Make graph start out centered on the Sun
    focus_body_final = orbital_bodies[focus_body]['prop_pos'][:, -1]
    fig.update_layout(scene=dict(
        xaxis=dict(range=[focus_body_final[0]-zoom_radius, focus_body_final[0]+zoom_radius], title='X (km)'),
        yaxis=dict(range=[focus_body_final[1]-zoom_radius, focus_body_final[1]+zoom_radius], title='Y (km)'),
        zaxis=dict(range=[focus_body_final[2]-zoom_height, focus_body_final[2]+zoom_height], title='Z (km)'),
        aspectmode='cube',   # keeps it from squashing orbits into ellipses
    ))

    if animate:
        # Currently breaks labels when including truth comparison
        n_times = orbital_bodies[focus_body]['prop_pos'].shape[1]
        frame_indices = list(range(0, n_times, frame_step))
        if frame_indices[-1] != n_times - 1:
            frame_indices.append(n_times - 1)
 
        frames = []
        for idx in frame_indices:
            frame_data = []
            for body in orbital_bodies:
                pos = orbital_bodies[body]['prop_pos']
                frame_data.append(go.Scatter3d(
                    x=pos[0, :idx + 1], y=pos[1, :idx + 1], z=pos[2, :idx + 1],
                    mode='lines',
                ))
                frame_data.append(go.Scatter3d(
                    x=[pos[0, idx]], y=[pos[1, idx]], z=[pos[2, idx]],
                    mode='markers', marker=dict(size=5),
                ))
                if orbital_bodies_truth_comparison is not None:
                    if body not in orbital_bodies_truth_comparison:
                        continue  # skip silently rather than crashing if truth data is missing for a body
                    truth_pos = orbital_bodies_truth_comparison[body].pos  # shape (n_times, 3)
                    frame_data.append(go.Scatter3d(
                    x=truth_pos[:idx+1,0], y=truth_pos[:idx+1,1], z=truth_pos[:idx+1,2],
                    mode='markers', marker=dict(size=2, symbol='x'), # Make exes instead of a line
                    ))
            frames.append(go.Frame(data=frame_data, name=str(idx)))
 
        fig.frames = frames
        fig.update_layout(updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[
                dict(label='Play', method='animate',
                     args=[None, {'frame': {'duration': 40, 'redraw': True}, 'fromcurrent': True}]),
                dict(label='Pause', method='animate',
                     args=[[None], {'frame': {'duration': 0}, 'mode': 'immediate'}]),
            ],
        )])

    fig.show()

def plot_pyplot(orbital_bodies):
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')

    for body in orbital_bodies:
        pos = orbital_bodies[body]['prop_pos']   # shape (3, n_times)
        ax.plot(pos[0], pos[1], pos[2], label=body)

    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.legend()
    ax.set_box_aspect([1, 1, 1])   # keeps orbits from looking squashed
    plt.show()


if __name__ == '__main__':
    print("\nplotting.py is a library module. Run 'python3 test_propagator.py --plot' to test.\n"
    "Or call plotting.plotly(orbital_bodies) or plotting.pyplot(orbital_bodies) to plot 3D data\n"
    "Where orbital_bodies is a dict of dicts as defined in constants.planet_params with pos added from propagator.py")