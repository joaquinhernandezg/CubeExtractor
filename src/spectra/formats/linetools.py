import numpy as np
import os
from linetools.spectra.xspectrum1d import XSpectrum1D
import astropy.units as u


class LinetoolsConverter:
    @staticmethod
    def spec_list_to_fits(spectra, out_filename_template="ID_{}_linetools_spectrum.fits", out_dir=".", overwrite=False):
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        for spec in spectra:
            flux = spec.data
            var = spec.var
            wave = spec.wave.coord()
            spec1d =  XSpectrum1D.from_tuple((wave, flux, np.sqrt(var)), verbose=False)
            specid = spec.primary_header["ID_OBJ"]
            out_filename = os.path.join(out_dir, out_filename_template.format(specid))
            spec1d.write_to_fits(out_filename)