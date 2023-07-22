import numpy as np
from astropy.io import fits
import os
from astropy.table import Table
from linetools.spectra.xspectrum1d import XSpectrum1D
import astropy.units as u
from scipy import interpolate

class RedMonsterConverter:
    @classmethod
    def spec_list_to_fits(cls, spectra, out_dir="./", overwrite=True):
        for spec in spectra:
            try:
                cls.spec_to_file(spec, out_dir=out_dir, overwrite=overwrite)
                print("Wrote spectrum", spec.primary_header["ID_OBJ"])
            except Exception as e:
                print(e)
                print("Couldn't save REDMONTER spectrum", spec.primary_header["ID_OBJ"])


    @staticmethod
    def spec_to_file(spectrum, out_filename=None, out_dir="./", overwrite=True):

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        wave = spectrum.wave.coord()
        flux = spectrum.data
        sig = np.sqrt(spectrum.var.data)
        sig[sig==0] = np.inf
        spec = XSpectrum1D.from_tuple((wave, flux, sig), verbose=False)


        wave_log = np.log10(wave)
        n = len(wave)
        spec.wavelength = wave_log * u.angstrom

        spec.sig = sig * spectrum.unit

        new_wave_log = np.arange(wave_log[1], wave_log[n - 2], 0.0001)
        spec_rebined = spec.rebin(new_wv=new_wave_log * u.angstrom)

        flux = spec_rebined.flux.value

        f = interpolate.interp1d(wave_log, sig)
        sig = f(new_wave_log)
        inv_sig = 1. / np.array(sig) ** 2
        inv_sig = np.where(np.isinf(inv_sig), 0, inv_sig)
        inv_sig = np.where(np.isnan(inv_sig), 0, inv_sig)
        hdu1 = fits.PrimaryHDU([flux])
        hdu2 = fits.ImageHDU([inv_sig])
        hdu1.header['COEFF0'] = new_wave_log[0]
        hdu1.header['COEFF1'] = new_wave_log[1] - new_wave_log[0]
        hdu1.header['MAG_R'] = 15

        hdu1.header['ID'] = spectrum.primary_header["ID_OBJ"]

        hdulist_new = fits.HDUList([hdu1, hdu2])

        if out_filename is None:
            out_filename = f"{spectrum.primary_header['ID_OBJ']}_RMF.fits"
        hdulist_new.writeto(os.path.join(out_dir, out_filename), overwrite=True)