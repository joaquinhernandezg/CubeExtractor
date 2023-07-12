from .base_extractor import ApertureExtractor


import astropy.units as u
from photutils.aperture import SkyEllipticalAperture
from astropy.coordinates import SkyCoord
import numpy as np
from astropy.io import fits



class CircularApertureExtractor(ApertureExtractor):
    @classmethod
    def get_apertures(cls, sextractor_catalog, min_axis_size_arcsec=0.4, aperture_factor=1,
                      ra_column="ALPHA_J2000", dec_column="DELTA_J2000", id_column="NUMBER"):
        ra_list, dec_list = sextractor_catalog[ra_column], sextractor_catalog[dec_column]
        apertures = []
        for ra, dec in zip(ra_list, dec_list):

            r = min_axis_size_arcsec/3600

            aperture = cls.get_aperture(min_axis_size_arcsec=min_axis_size_arcsec, aperture_factor=aperture_factor, ra=ra, dec=dec)
            apertures.append(aperture)

        return apertures

    @classmethod
    def get_aperture(cls, ra, dec, min_axis_size_arcsec=0.4, aperture_factor=1,):
        r = min_axis_size_arcsec/3600
        pos_angle = 0
        pos_angle =0

        position = SkyCoord(ra=ra, dec=dec, unit='deg')
        aperture = SkyEllipticalAperture(position, r*u.deg, r*u.deg,  pos_angle*u.rad)
        return aperture




class EllipticalApertureExtractor(ApertureExtractor):

    @classmethod
    def get_apertures(cls, sextractor_catalog, min_axis_size_arcsec=0.4, aperture_factor=1, ra_column="ALPHA_J2000", dec_column="DELTA_J2000", id_column="NUMBER"):
        ra_list, dec_list = sextractor_catalog[ra_column], sextractor_catalog[dec_column]
        a_list, b_list, pos_angle_list = sextractor_catalog["A_WORLD"], sextractor_catalog["B_WORLD"], sextractor_catalog["THETA_J2000"]
        apertures = []
        for ra, dec, a, b, pos_angle in zip(ra_list, dec_list, a_list, b_list, pos_angle_list):
            a, b = a*aperture_factor, b*aperture_factor
            if b < min_axis_size_arcsec/3600:
                a, b = a/b*min_axis_size_arcsec/3600, min_axis_size_arcsec/3600

            pos_angle =np.deg2rad(pos_angle)

            aperture = cls.get_aperture(ra=ra, dec=dec, a=a, b=b, pos_angle=pos_angle, min_axis_size_arcsec=min_axis_size_arcsec, aperture_factor=aperture_factor)

        return apertures

    @classmethod
    def get_aperture(cls, ra, dec, a, b, pos_angle, min_axis_size_arcsec=0.4, aperture_factor=1):
        a, b = a*aperture_factor, b*aperture_factor
        if b < min_axis_size_arcsec/3600:
            a, b = a/b*min_axis_size_arcsec/3600, min_axis_size_arcsec/3600

        pos_angle =np.deg2rad(pos_angle)

        position = SkyCoord(ra=ra, dec=dec, unit='deg')
        aperture = SkyEllipticalAperture(position, a*u.deg, b*u.deg,  pos_angle*u.rad)
        return aperture


