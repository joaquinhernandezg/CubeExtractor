from mpdaf.obj import Cube, Spectrum, Image
import numpy as np
import os
from astropy.io import fits
from ..spectra.formats import MarzConverter, LinetoolsConverter, RedMonsterConverter

def make_white_image(cube, out_filename=None, mask_nans=True, wave_min=None, wave_max=None):
    if isinstance(cube, str):
        cube = Cube(cube)
    if not isinstance(cube, Cube):
        raise ValueError("cube must be a path to a cube or a Cube instance")

    if mask_nans:
        cube.data[np.isnan(cube.data)] = 0
        cube.var[np.isnan(cube.data)] = np.inf

    #TODO: add the cases where wave_min or wave_max are None, take them as the min and max of the cube
    if wave_min is not None and wave_max is not None:
        cube = cube.select_lambda(wave_min, wave_max)

    white = cube.sum(axis=0)
    white.var[white.var==0] = 0
    if isinstance(out_filename, str):
        white.write(out_filename )
    return white

def write_cutouts(spectra_list, out_dir, overwrite=True):
    """Writes a list of spectra to a FITS file.

    Parameters
    ----------
    spectra : list
        The list of spectra to write to the FITS file.
    """

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for spec in spectra_list:
        hdul = fits.HDUList()

        white = spec.white_cutout.data
        mask = spec.mask_cutout
        weight = spec.weight_cutout
        hdul.append(fits.PrimaryHDU())
        if white is not None:
            hdul.append(fits.ImageHDU(np.array(white)))
        if mask is not None:
            hdul.append(fits.ImageHDU(np.array(mask)))
        if weight is not None:
            hdul.append(fits.ImageHDU(np.array(weight)))

        hdul.writeto(os.path.join(out_dir, str(spec.primary_header["ID_OBJ"]).zfill(4) + ".fits"), overwrite=overwrite)


def write_extraction_data(spectra_list, out_cutous_dir=None, marz_table_filename=None,
                          linetools_outdir=None, redmonster_outdir=None, overwrite=False):


    if out_cutous_dir:
        write_cutouts(spectra_list, out_cutous_dir, overwrite=overwrite)

    if marz_table_filename:
        MarzConverter.spec_list_to_fits(spectra_list, out_filename=marz_table_filename, overwrite=overwrite)

    if linetools_outdir:
        LinetoolsConverter.spec_list_to_fits(spectra_list, out_dir=linetools_outdir, overwrite=overwrite)

    if redmonster_outdir:
        RedMonsterConverter.spec_list_to_fits(spectra_list, out_dir=redmonster_outdir, overwrite=overwrite)

