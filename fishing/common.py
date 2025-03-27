from dataclasses import dataclass

import numpy as np


@dataclass
class Species:
    idx: int
    population: int
    centroid: np.ndarray
    sigma: float
