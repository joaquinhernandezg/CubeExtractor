import astropy.units as u
import numpy as np

class BaseWeights:

    @classmethod
    def get_weights(cls, masked_cube, white, weight_window=(None, None), *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_wave_and_wmin_wmax(cls, masked_cube, weight_window=(None, None)):
        range = masked_cube.get_range(unit_wave=u.angstrom)
        wave_step = masked_cube.get_step(unit_wave=u.angstrom)[0]

        #Note, add 10percent of step to the max wavelength to include that last pixel.
        wave = np.arange(range[0], range[3]+0.1*wave_step, wave_step)
        wmin = np.min(wave)
        wmax = np.max(wave)

        if isinstance(weight_window[0], float):
                if weight_window[0]>wmin and weight_window[0]<np.max(wave):
                    wmin = weight_window[0]
        if isinstance(weight_window[1], float):
                if weight_window[1]<wmax and weight_window[1]>np.min(wave):
                    wmax = weight_window[1]
        return wave, wmin, wmax
