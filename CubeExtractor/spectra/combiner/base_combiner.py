from astropy.table import Table
from mpdaf.obj import Cube, Spectrum, Image
import matplotlib.pyplot as plt
import astropy.units as u
from photutils.aperture import EllipticalAperture, SkyEllipticalAperture
from astropy.coordinates import SkyCoord
import numpy as np
from astropy.io import fits
import os
import astropy.units as u

from ..weighter import (NoWeights, FluxWeighths,
IVarWeights, SNRWeights)

import unittest


class SimpleCubeSpectraCombiner:
    METHOD = "sum"

    @classmethod
    def combine(cls, masked_cube, white, combine_method="mean", weighter=None, *weighter_args, **weighter_kwargs):

        #TODO: move this to somewhere else
        if weighter == "None":
            weighter = NoWeights
        elif weighter == "flux":
            weighter = FluxWeighths
        elif weighter == "ivar":
            weighter = IVarWeights
        #elif weighter == "robertson":
        #    weighter = RobertsonWeights
        elif weighter == "snr":
            weighter = SNRWeights
        else:
            raise ValueError("Weighter not recognized")

        weights = weighter.get_weights(masked_cube, white, *weighter_args, **weighter_kwargs)
        if not weights.any():
            return None, None

        masked_cube.data[np.isnan(masked_cube.data)] = 0
        masked_cube.var[np.isnan(masked_cube.var)] = 0
        weights[np.isnan(weights)] = 0

        if combine_method:
            method = getattr(masked_cube*weights, combine_method)
        else:
            method = getattr(masked_cube*weights, cls.METHOD)

        spec = method(axis=(1, 2))
        return spec, weights