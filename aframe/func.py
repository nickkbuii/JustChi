# useful functions for calculation

import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle(p1, mid, p2):
    v1_u = unit_vector(p1 - mid)
    v2_u = unit_vector(p2 - mid)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def similarity(ground_truth, deg_freedom, angle): return ground_truth - deg_freedom <= angle <= ground_truth + deg_freedom