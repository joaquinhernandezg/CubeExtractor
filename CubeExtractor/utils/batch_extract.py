from mpdaf.obj import Cube, Spectrum, Image
from astropy.table import Table
from astropy.io import fits
import os
import traceback
import logging
import numpy as np


def extract_batch_spectra(cube_filename, white_filename, catalog_filename, aperture_extractor, combine_method="sum", weight_method=None,
                  ra_column="RA", dec_column="DEC", id_column="ID",
                  a_column="A_WORLD", b_column="B_WORLD", theta_column="THETA_WORLD",
                  radius_column="FLUX_RADIUS", radius_factor=1.0,
                  segmentation_mask_filename=None,
                  skip_exceptions=False, extract_only_n=-1, var_image=None,
                  *args, **kwargs):
    """Extracts a batch of spectra from a cube and a catalog of sources.

    Parameters
    ----------
    cube : `~mpdaf.obj.Cube`
        The cube to extract the spectra from.
    white : `~mpdaf.obj.Image`
        The white image to use for the extraction.
    catalog : `~astropy.table.Table`
        The catalog of sources to extract the spectra from.
    aperture_extractor : `~mpdaf.sdetect.ApertureExtractor`
        The aperture extractor to use to extract the spectra.
    combine_method : str
        The method to use to combine the spectra. See
        `~mpdaf.sdetect.SimpleCubeSpectraCombiner.combine` for details.
    weight_method : str
        The method to use to weight the spectra. See
        `~mpdaf.sdetect.SimpleCubeSpectraCombiner.combine` for details.
    ra_column : str
        The name of the column in the catalog that contains the right
        ascension of the sources.
    dec_column : str
        The name of the column in the catalog that contains the declination
        of the sources.
    id_column : str
        The name of the column in the catalog that contains the IDs of the
        sources.
    segmentation_mask : `~numpy.ndarray`
        The segmentation mask to use for the extraction.

    Returns
    -------
    spectra : `~astropy.table.Table`
        The extracted spectra.
    """
    # handle cases of elliptical apertures
    cube = Cube(cube_filename)
    cube.var.data[cube.var.data==0] = np.inf

    white = Image(white_filename)

    if var_image is not None:
        print(var_image)
        var = fits.getdata(var_image)
        white = white.new_from_obj(white, var=var)

    sources_catalog = Table.read(catalog_filename)
    segmentation_mask = fits.getdata(segmentation_mask_filename) if segmentation_mask_filename else None

    if extract_only_n > 0:
        sources_catalog = sources_catalog[0:extract_only_n]
    spectra_list = []
    for i in range(len(sources_catalog)):
        logging.info("Extracting spectrum: ID: {}, {}/{}".format(sources_catalog[id_column][i], i+1, len(sources_catalog)))
        ra = sources_catalog[ra_column][i]
        dec = sources_catalog[dec_column][i]
        source_id = sources_catalog[id_column][i]
        a, b = sources_catalog[a_column][i], sources_catalog[b_column][i]
        radius = sources_catalog[radius_column][i]/3600*radius_factor
        ax_ratio = b/a
        a, b = radius/np.sqrt(ax_ratio), radius*np.sqrt(ax_ratio)
        theta = np.deg2rad(sources_catalog[theta_column][i])


        mask = segmentation_mask == source_id if segmentation_mask is not None else None


        try:
            spec = aperture_extractor.extract_single(cube=cube, white=white, ra=ra, dec=dec,
                                                     spectrum_id=source_id, segmentation_mask=mask,
                                                     combine_method=combine_method, weight_method=weight_method,
                                                     a=a, b=b,
                                                     pos_angle=theta,
                                                     radius=radius,
                                                     *args, **kwargs)
        except Exception as e:
            if not skip_exceptions:
                raise e
            else:
                print("Exception raised while extracting spectrum: ID: {}".format(source_id))
                traceback.print_exc()
                spec = None

        spectra_list.append(spec)

    return spectra_list






