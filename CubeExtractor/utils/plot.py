import matplotlib.pyplot as plt
from ..spectra.extractor import (CircularApertureExtractor,MaskExtractor, EllipticalApertureExtractor)

from astropy.visualization import ZScaleInterval
from photutils.segmentation import SegmentationImage



def plot_apertures(white_image, catalog, ra_column, dec_column, id_column,
                   aperture_extractor=None, segmentation_mask=None, fig=None, ax=None, aperture_params_dict={},
                   *imshow_args, **imshow_kwargs):
    if fig is None or ax is None:
        fig, ax = plt.subplots()

    vmin, vmax = ZScaleInterval().get_limits(white_image.data)
    ax.imshow(white_image.data, origin="lower", cmap="gray", vmin=vmin, vmax=vmax,
              *imshow_args, **imshow_kwargs)

    if segmentation_mask is not None:
        segm = SegmentationImage(segmentation_mask)
        ax.imshow(segmentation_mask, origin="lower", alpha=0.8, cmap=segm.make_cmap(seed=0, background_color=(0, 0, 0, 0.1)))

    if aperture_extractor is not None and aperture_extractor != MaskExtractor:
        sky_apertures = aperture_extractor.get_apertures(catalog, ra_column=ra_column, dec_column=dec_column, id_column=id_column)

        if sky_apertures is not None:
            pix_apertures = list(map(lambda aperture:aperture.to_pixel(white_image.wcs.wcs), sky_apertures))

            for i, aperture in enumerate(pix_apertures):
                aperture.plot(axes=ax, **aperture_params_dict)
                x, y = aperture.positions
                ax.text(x, y, catalog[id_column][i])

    return fig, ax
