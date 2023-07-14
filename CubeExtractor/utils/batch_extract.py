from mpdaf.obj import Cube, Spectrum, Image
from astropy.table import Table
from astropy.io import fits
import os
import traceback



def extract_batch_spectra(cube_filename, white_filename, catalog_filename, aperture_extractor, combine_method="sum", weight_method=None,
                  ra_column="RA", dec_column="DEC", id_column="ID",
                  segmentation_mask_filename=None,
                  skip_exceptions=False, extract_only_n=-1,
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
    cube = Cube(cube_filename)
    white = Image(white_filename)
    sources_catalog = Table.read(catalog_filename)
    segmentation_mask = fits.getdata(segmentation_mask_filename) if segmentation_mask_filename else None

    if extract_only_n > 0:
        sources_catalog = sources_catalog[0:extract_only_n]
    spectra_list = []
    for i in range(len(sources_catalog)):
        ra = sources_catalog[ra_column][i]
        dec = sources_catalog[dec_column][i]
        source_id = sources_catalog[id_column][i]

        mask = segmentation_mask == source_id if segmentation_mask is not None else None

        try:
            spec = aperture_extractor.extract_single(cube=cube, white=white, ra=ra, dec=dec,
                                                     spectrum_id=source_id, segmentation_mask=mask,
                                                     combine_method=combine_method, weight_method=weight_method, *args, **kwargs)
        except Exception as e:
            if not skip_exceptions:
                raise e
            else:
                print("Exception raised while extracting spectrum: ID: {}".format(source_id))
                traceback.print_exc()
                spec = None

        spectra_list.append(spec)

    return spectra_list






