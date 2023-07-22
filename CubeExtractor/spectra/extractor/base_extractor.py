from mpdaf.obj import Image
import matplotlib.pyplot as plt
import numpy as np

from ..combiner.base_combiner import SimpleCubeSpectraCombiner

class ApertureExtractor:
    @staticmethod
    def subwhite_from_mask(white, mask, segmentation_mask=None):
        """Extract a subcube from a cube given a mask.
        It is assumed that the mask is a boolean array with the same shape as the cube.
        The mask is assumed to have only one object masked of an arbitrary shape, and
        the masked object edges are used to extract the subcube.

        Parameters
        ----------
        cube : np.ndarray or mpdaf.obj.Cube
            Cube from wich the subcube is extracted.
        mask : np.ndarray
            2D boolean array with the same shape as the cube.

        Returns
        -------
        np.ndarray or mpdaf.obj.Cube
            The extracted subcube
        """
        if segmentation_mask is not None:
            mask *= segmentation_mask

        where = np.array(np.where(mask))

        y1, x1 = np.amin(where, axis=1)
        y2, x2 = np.amax(where, axis=1)

        subwhite = white[y1:y2+1, x1:x2+1]
        return subwhite


    @classmethod
    def subwhite(cls, white, aperture=None, segmentation_mask=None):
        """Extract a subcube based on an aperture. The aperture is a pixel aperture
        from photutils.aperture.Aperture.PixelAperture. The subcube is extracted
        based on the mask edges of the aperture.

        Parameters
        ----------
        cube : np.ndarray or mpdaf.obj.Cube
            Cube from wich the subcube is extracted.
        aperture : photutils.aperture.Aperture.PixelAperture
            The aperture object used to create the subcube.

        Returns
        -------
        np.ndarray or mpdaf.obj.Cube
            Subcube with masked pixels outside the defined aperture
        """
        if aperture is not None:
            mask = aperture.to_mask(method="center").to_image(white.shape)
        else:
            mask = np.ones(white.shape)

        return cls.subwhite_from_mask(white, mask, segmentation_mask=segmentation_mask)


    @staticmethod
    def subcube_from_mask(cube, mask, segmentation_mask=None):
        """Extract a subcube from a cube given a mask.
        It is assumed that the mask is a boolean array with the same shape as the cube.
        The mask is assumed to have only one object masked of an arbitrary shape, and
        the masked object edges are used to extract the subcube.

        Parameters
        ----------
        cube : np.ndarray or mpdaf.obj.Cube
            Cube from wich the subcube is extracted.
        mask : np.ndarray
            2D boolean array with the same shape as the cube.

        Returns
        -------
        np.ndarray or mpdaf.obj.Cube
            The extracted subcube
        """
        if segmentation_mask is not None:
            mask *= segmentation_mask

        where = np.array(np.where(mask))

        y1, x1 = np.amin(where, axis=1)
        y2, x2 = np.amax(where, axis=1)

        subcube = cube[:, y1:y2+1, x1:x2+1]
        subcube.mask = np.tile(np.logical_not(mask[y1:y2+1, x1:x2+1]), (cube.shape[0], 1, 1))

        return subcube


    @classmethod
    def subcube(cls, cube, aperture=None, segmentation_mask=None):
        """Extract a subcube based on an aperture. The aperture is a pixel aperture
        from photutils.aperture.Aperture.PixelAperture. The subcube is extracted
        based on the mask edges of the aperture.

        Parameters
        ----------
        cube : np.ndarray or mpdaf.obj.Cube
            Cube from wich the subcube is extracted.
        aperture : photutils.aperture.Aperture.PixelAperture
            The aperture object used to create the subcube.

        Returns
        -------
        np.ndarray or mpdaf.obj.Cube
            Subcube with masked pixels outside the defined aperture
        """
        if aperture is not None:
            mask = aperture.to_mask(method="center").to_image(cube.shape[1:])
        else:
            mask = np.ones(cube.shape[1:])

        return cls.subcube_from_mask(cube, mask, segmentation_mask=segmentation_mask)


    @classmethod
    def build_mask(cls, cube, sky_aperture=None, segmentation_mask=None):
        """Generate a mask with the same shape a the cube slices.
        The mask is 1 where the spaxels are to be considered and 0 where they are not.
        Mask is constructed from the sky_aperture and the segmentation_mask.

        Parameters
        ----------
        cube : mdaf.obj.Cube
            Cube from wich the mask is built.
        sky_aperture : _type_, optional
            , by default None
        segmentation_mask : np.ndarray, optional
            Segmentation mask denoting the region where there is flux, by default None

        Returns
        -------
        np.ndarray
            Mask containing 1 where the spaxels are to be considered and 0 where they are not.
        """

        # default mask is all 1
        mask = np.ones(cube.shape[1:])

        # if there is a sky aperture
        if sky_aperture is not None:
            # create a pixel aperture
            pix_aperture = sky_aperture.to_pixel(cube[0].wcs.wcs)
            # calculate the mask covering the aperture and update the mask
            mask *= pix_aperture.to_mask(method="center").to_image(cube.shape[1:]).astype(int)

        # if there is segmentation mask
        if segmentation_mask is not None:
            # mask everything outside the segmentation
            mask *= segmentation_mask
        return mask


    @classmethod
    def extract_single(cls, cube, white, ra, dec, spectrum_id, combine_method="sum", weight_method=None, segmentation_mask=None, *args, **kwargs):
        """Extract a single spectra from a IFU cube

        Parameters
        ----------
        cube : mpdaf.obj.Cube
            MUSE cube from where to extract the spectra.
            Should have a data and var attributes, and a correct WCS.
        ra : float
            Right Ascencion of the source, in degrees.
        dec : float
            Declination of the source, in degrees.
        spectrum_id : int
            ID of the source to extract.
        combine_method : str, optional
           Method to combine the spectra in the defined region, by default "sum".
           Can be "mean", "median", "sum".
        weight_method : float, optional
            Weigthing algorithm to calculate the weights of each spaxel
            in the defind region, by default None. Can be None (equal weights),
            snr, flux, ivar.
        segmentation_mask : numpy.array, optional
            2D Mask defining the region of the spaxels to combine in the cube.
            , by default None. If passed, only the spaxels at mask==1 are considered
            in the spaxel combination. If None, all the spaxels are taken into account.
        *args, **kwargs: tuple, dict, optional
            Arguments passed to each specific child class of ApertureExtractor.
            e.g. circular apertures require ra, dec, radius, but elliptical apertures
            require a,b,theta,ra,dec.

        Returns
        -------
        _type_
            _description_
        """
        # define the aperture object
        aperture = cls.get_aperture(ra, dec, *args, **kwargs)
        # calculates the mask defined by the aperture
        mask = cls.build_mask(cube, aperture, segmentation_mask=segmentation_mask)
        # construct the subcube enclosing the mask
        subcube = cls.subcube_from_mask(cube, mask)
        subwhite = cls.subwhite_from_mask(white, mask)
        # extract the spectrum
        spec, weights = SimpleCubeSpectraCombiner.combine(subcube, subwhite, combine_method=combine_method, weighter=weight_method)
        if spec is None or weights is None:
            return None

        # saves some basic information in the spectrum's header
        spec.primary_header["RA_OBJ"] = ra
        spec.primary_header["DEC_OBJ"] = dec
        spec.primary_header["ID_OBJ"] = spectrum_id
        subcube.unmask()
        setattr(spec, "white_cutout", np.nansum(subcube.data, axis=0))
        setattr(spec, "mask_cutout", mask)
        setattr(spec, "weight_cutout", weights)
        return spec



    @classmethod
    def plot_apertures(cls, image_filename, sources_catalog, aperture_params_dict={}, ra_column="ALPHA_J2000", dec_column="DELTA_J2000", id_column="NUMBER",
                       ax=None, fig=None, **imshow_params):
        im = Image(image_filename)
        apertures = cls.get_apertures(sources_catalog, ra_column=ra_column, dec_column=dec_column, id_column=id_column)

        if apertures is not None:
            apertures = list(map(lambda aperture:aperture.to_pixel(im.wcs.wcs), apertures))

        vmin, vmax = ZScaleInterval().get_limits(im.data)
        if ax is None:
            fig, ax = plt.subplots()
        im.plot(ax=ax, vmin=vmin, vmax=vmax, **imshow_params)

        if apertures is not None:
            for i, aperture in enumerate(apertures):
                aperture.plot(axes=ax, **aperture_params_dict)
                x, y = aperture.positions
                ax.text(x, y, sources_catalog[id_column][i])

        return fig

    @classmethod
    def get_apertures(cls, sextractor_catalog, *args, **kwargs):
        raise NotImplementedError("Not supported yet")

    @classmethod
    def get_aperture(cls, ra, dec, *args, **kwargs):
        raise NotImplementedError("Not supported yet")
