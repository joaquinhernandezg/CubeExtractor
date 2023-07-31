from .base_extractor import ApertureExtractor


import astropy.units as u
from photutils.aperture import SkyEllipticalAperture
from astropy.coordinates import SkyCoord
import numpy as np
from astropy.io import fits



class EllipticalApertureExtractor(ApertureExtractor):

    @classmethod
    def get_apertures(cls, sextractor_catalog, radius_factor=1, radius_column="FLUX_RADIUS", ra_column="ALPHA_J2000", dec_column="DELTA_J2000",
                      a_column="A_WORLD", b_column="B_WORLD", theta_column="THETA_WORLD", *args, **kwargs):
        ra_list, dec_list = sextractor_catalog[ra_column], sextractor_catalog[dec_column]
        a_list, b_list, pos_angle_list = sextractor_catalog[a_column], sextractor_catalog[b_column], sextractor_catalog[theta_column]
        radii = sextractor_catalog[radius_column]*radius_factor
        apertures = []
        for ra, dec, radius, a, b, pos_angle in zip(ra_list, dec_list, radii, a_list, b_list, pos_angle_list):
            if radius <= 0 or a<=0 or b<=0:
                print("Negative radius")
                continue
            ax_ratio = b/a
            a, b = radius/3600/np.sqrt(ax_ratio), radius/3600*np.sqrt(ax_ratio)

            pos_angle =np.deg2rad(pos_angle)

            aperture = cls.get_aperture(ra=ra, dec=dec, a=a, b=b, pos_angle=pos_angle)
            apertures.append(aperture)
        return apertures

    @classmethod
    def get_aperture(cls, ra, dec, a, b, pos_angle, *args, **kwargs):
        position = SkyCoord(ra=ra, dec=dec, unit='deg')
        aperture = SkyEllipticalAperture(position, a*u.deg, b*u.deg,  pos_angle*u.rad)
        return aperture


class CircularApertureExtractor(EllipticalApertureExtractor):
    @classmethod
    def get_apertures(cls, sextractor_catalog, radius_column="FLUX_RADIUS", radius_factor=1,
                      ra_column="ALPHA_J2000", dec_column="DELTA_J2000", *args, **kwargs):
        ra_list, dec_list = sextractor_catalog[ra_column], sextractor_catalog[dec_column]
        radii = sextractor_catalog[radius_column]*radius_factor/3600
        apertures = []
        for ra, dec, radius in zip(ra_list, dec_list, radii):
            if radius < 0:
                print("Negative radius")
                continue
            aperture = cls.get_aperture(ra=ra, dec=dec, a=radius, b=radius, pos_angle=0)
            apertures.append(aperture)
        return apertures

