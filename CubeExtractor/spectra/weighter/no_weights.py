import numpy as np
from .base_weights import BaseWeights

class NoWeights(BaseWeights):
    @classmethod
    def get_weights(cls, masked_cube, white, weight_window=(None, None), *args, **kwargs):
        ws = np.ones(masked_cube.shape[1:])
        ws = ws
        return ws


