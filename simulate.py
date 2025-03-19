import numpy as np
import plotly.graph_objects as go


def generate_fish(
    n_species: int = 2, fish_per_species: int = 5, sigma: float = 0.5,
    plot: bool = False
) -> np.ndarray:
    """Generate numeric representations of the fish. This starts from the
    assumption that the fish are relatively independent, and so projects them
    into a space orthogonal by species. Thus, individuals of a species only
    vary along their species' direction.

    Parameters
    ----------
    n_species : int, optional
        How many species of fish there are, by default 2.
    fish_per_species : int, optional
        How many individuals should be generated per species, by default 5.
        TODO: allow array entries here so that different species can more
        individuals than others.
    sigma : float, optional
        How much variation intra-species variation there is, by default 0.5.
    plot : bool, optional
        Whether or not to scatter plot the first 2 dimensions of the fish, by
        default False.

    Returns
    -------
    fish : np.ndarray
        The numeric descriptions of the fish.
    """
    fish = np.zeros(shape=(n_species * fish_per_species, n_species))
    for j in range(n_species):
        i0 = j * fish_per_species
        i1 = (j + 1) * fish_per_species
        fish[i0:i1, j] = 1 - sigma * np.random.rand(fish_per_species)

    if plot:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=fish[:, 0], y=fish[:, 1],
                mode='markers',
            )
        )
        fig.update_layout(
            template='simple_white', width=1000, height=800,
            title='Fish',
            xaxis_title='$c_1$', yaxis_title='$c_2$'
        )
        fig.show()

    return fish


if __name__ == '__main__':
    fish = generate_fish(plot=True)
