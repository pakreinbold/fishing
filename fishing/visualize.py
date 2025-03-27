import numpy as np
import plotly.graph_objects as go

from fishing.common import Species


def visualize_fish_and_bait(all_species: list[Species], baits: np.ndarray):
    fig = go.Figure()

    const = np.sqrt(5.991)
    for species in all_species:
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=species.centroid[0] - species.sigma * const,
            x1=species.centroid[0] + species.sigma * const,
            y0=species.centroid[1] - species.sigma * const,
            y1=species.centroid[1] + species.sigma * const,
            opacity=0.2,
            fillcolor="grey",
            line_color="grey",
        )
        fig.add_trace(
            go.Scatter(
                x=[species.centroid[0]], y=[species.centroid[1]],
                mode='markers', name=f"Species {species.idx}",
            )
        )

    for i, bait in enumerate(baits):
        fig.add_trace(
            go.Scatter(
                x=[bait[0]], y=[bait[1]],
                mode='markers', name=f'Bait {i}',
                marker=dict(
                    symbol='diamond',
                    color='blue',
                )
            )
        )

    fig.update_layout(
        template='simple_white', width=1000, height=800,
        title='Fish',
        xaxis=dict(title='$c_1$', range=[0, 1]),
        yaxis=dict(title='$c_2$', range=[0, 1]),
    )
    fig.show()
