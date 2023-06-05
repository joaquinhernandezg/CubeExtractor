
import numpy as np
import os
from astropy.table import Table


class AsciiConverter:
    @staticmethod
    def spec_list_to_ascii(spectra, out_filename_template="spectra_{}.ascii", out_dir=".", overwrite=False):
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        for spec in spectra:
            flux = spec.data
            var = spec.var
            wave = spec.wave.coord()
            specid = spec.primary_header["ID_OBJ"]
            data_dict = {"wave": wave, "flux":flux, "error":np.sqrt(var)}
            table = Table(data_dict)

            out_filename = os.path.join(out_dir, out_filename_template.format(specid))
            table.write(out_filename, format="ascii", overwrite=True)
