import numpy as np
from .base_weights import BaseWeights


class FluxWeighths(BaseWeights):

    @classmethod
    def get_weights(cls, masked_cube, white, weight_window=(None, None)):
        wave, wmin, wmax = cls.get_wave_and_wmin_wmax(masked_cube, weight_window=weight_window)

        winds = (wave>=wmin) * (wave<=wmax)

        #Create the weights
        mask = np.logical_not(masked_cube.mask[0])
        data = white.data*mask
        var =white.var*mask

        ws = np.nansum(data[winds,:,:]*mask, axis=0)
        ws *= (ws>0)
        ws = ws
        return ws
