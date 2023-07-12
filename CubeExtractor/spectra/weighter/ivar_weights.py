import numpy as np
from .base_weights import BaseWeights


class IVarWeights(BaseWeights):

    @classmethod
    def get_weights(cls, masked_cube, white, weight_window=(None, None)):
        wave, wmin, wmax = cls.get_wave_and_wmin_wmax(masked_cube, weight_window=weight_window)
        #Create the weights
        mask = np.logical_not(masked_cube.mask[0])
        data = masked_cube.data*mask
        var = masked_cube.var*mask
        winds = (wave>=wmin) * (wave<=wmax)

        ws = np.nansum(1.0/var[winds,:,:]*(var[winds,:,:]>0.0), axis=0)
        ws = ws
        return ws
