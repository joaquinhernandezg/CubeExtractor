import numpy as np
from .base_weights import BaseWeights

class SNRWeights(BaseWeights):
    @classmethod
    def get_weights(cls, masked_cube, white, weight_window=(None, None)):
        if masked_cube.wcs is not None and weight_window!=(None, None):
            wave, wmin, wmax = cls.get_wave_and_wmin_wmax(masked_cube, weight_window=weight_window)

            winds = (wave>=wmin) * (wave<=wmax)
        else:
            winds = np.ones(masked_cube.shape[0], dtype=bool)

        #Create the weights
        mask = np.logical_not(masked_cube.mask[0])
        data = white.data*mask
        var = white.var*mask

        snr = data/np.sqrt(var)
        snr *= (snr>0)
        ws = snr
        ws = ws/np.nansum(ws)
        ws = np.tile(ws, (masked_cube.shape[0], 1, 1))
        return ws
