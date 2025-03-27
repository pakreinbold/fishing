"""TODO: Add ponds, which have different population levels of the different fish species."""
import numpy as np
import pandas as pd

from fishing.common import Species
from fishing.save import insert_rows_to_bq


def _compute_probs(
    fish: np.ndarray,
    baits: np.ndarray,
    lam: float = 0.01,
    normalize: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    assert fish.shape[0] == baits.shape[1], "Fish and Bait must exist in the same space"
    dists = baits - fish[None, :]
    dists = np.sqrt(dists[:, 0]**2 + dists[:, 1]**2)
    probs = np.exp(-dists**2 / lam)
    if normalize:
        probs /= probs.sum()
    return probs, dists


def generate_species(
    n_species: int = 3,
    population_range: tuple[int, int] = (10, 25),
    n_dims: int = 2,
    sigma_range: tuple[float, float] = (0.05, 0.1),
) -> list[Species]:
    all_species = []
    for n in range(n_species):
        all_species.append(
            Species(
                idx=n,
                population=np.random.randint(population_range[0], population_range[1]),
                centroid=np.random.rand(n_dims),
                sigma=(sigma_range[1] - sigma_range[0]) * np.random.rand() + sigma_range[0],
            )
        )
    return all_species


def generate_bait(ndims: int = 2, nbait: int = 10):
    return np.random.rand(nbait, ndims)


def simulate_fishing(all_species: list[Species], baits: np.ndarray) -> pd.DataFrame:
    """Species are defined by a centroid and standard deviation in some space. Individuals of a
    species are drawn from a Gaussian distribution centered at the centroid and with the standard
    deviation. Then, the fish will iteratively look at the available bait, in order of closest to
    furthest. Every time it looks at a bait, it will bit with probability inversely related to its
    distance to that bait. If it bites a bait, then it is caught, and we move on to the next fish.
    Otherwise, it looks at the next bait. Each individual for every species proceeds in this manner
    until they are either caught or exhaust their bait options. If they exhaust their bait options,
    then they 'get away'.

    Parameters
    ----------
    all_species : list[Species]
        _description_
    baits : np.ndarray
        _description_

    Returns
    -------
    pd.DataFrame
        _description_
    """
    bites = []
    for species in all_species:
        for i in range(species.population):
            # Generate individual and compare it to bait
            fish = species.centroid + species.sigma * np.random.randn(2,)
            probs, dists = _compute_probs(fish, baits, normalize=False)

            # See if it bites anything
            bait = -1
            n_chances = 0
            for j in np.argsort(dists):
                n_chances += 1
                if np.random.rand() <= probs[j]:
                    bait = j
                    break

            bites.append(
                {'species': species.idx, 'fish': i, 'bait': bait, 'n_chances': n_chances}
            )

            # Logging
            if bait >= 0:
                print(
                    f"\n Fish {species.idx}-{i} ({fish[0]:.2f}"
                    f", {fish[1]:.2f}) bit Bait {bait} ({baits[bait, 0]:.2f}, {baits[bait, 1]:.2f})"
                    f", because it was {dists[bait]:.3f} away with p={probs[j]:.3f}"  # type: ignore
                )
            else:
                print(f"\n Fish{species.idx}-{i} did not bite anything!")

    return pd.DataFrame(bites)


if __name__ == '__main__':
    all_species = generate_species()
    baits = generate_bait()
    bites = simulate_fishing(all_species, baits)

    import datetime as dt
    bites['create_date'] = dt.date.today().strftime("%Y-%m-%d")
    insert_rows_to_bq("bites", bites.to_dict('records'))
