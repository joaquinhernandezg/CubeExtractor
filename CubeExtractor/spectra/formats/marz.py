from astropy.io import fits
from astropy.table import Table
import numpy as np

class MarzConverter:
    @staticmethod
    def spec_list_to_fits(spectra, out_filename="marz_spectra.fits", overwrite=False):
        wave_header = spectra[0].wave.to_header()

        data_matrix = np.array([spec.data for spec in spectra ])
        variance_matrix = np.array([spec.var for spec in spectra])

        ra_list = np.array(list(map(lambda spec:spec.primary_header["RA_OBJ"]/360*2*np.pi, spectra)))
        dec_list = np.array(list(map(lambda spec:spec.primary_header["DEC_OBJ"]/360*2*np.pi, spectra)))
        name = list(map(lambda spec:str(spec.primary_header["ID_OBJ"]), spectra))
        type_list = ["P"]*len(spectra)
        magnitudes = np.zeros(len(spectra))
        comments = [""]*len(spectra)


        table = Table([type_list, name, ra_list, dec_list, magnitudes, comments], names=("TYPE", 'NAME', 'RA', 'DEC', "MAGNITUDE", "COMMENT"))

        data_ext = fits.ImageHDU(data=data_matrix, header=wave_header)
        data_ext.name = "intensity"

        var_ext = fits.ImageHDU(data=variance_matrix, header=wave_header)
        var_ext.name = "variance"

        table_ext = fits.BinTableHDU(data=table)
        table_ext.name = "fibres"

        hdul = fits.HDUList([fits.PrimaryHDU(header=wave_header), data_ext, var_ext, table_ext])
        hdul.writeto(out_filename, overwrite=True)
