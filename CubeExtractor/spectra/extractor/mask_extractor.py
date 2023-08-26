from .base_extractor import ApertureExtractor
from ..combiner import SimpleCubeSpectraCombiner

import numpy as np

class MaskExtractor(ApertureExtractor):
    @classmethod
    def extract_single(cls, cube, white, ra, dec, spectrum_id, combine_method="sum",
                       weight_method=None, segmentation_mask=None,*args, **kwargs):
        mask = cls.build_mask(cube, sky_aperture=None, segmentation_mask=segmentation_mask)
        subcube = cls.subcube_from_mask(cube, mask)
        subwhite = cls.subwhite_from_mask(white, mask)
        spec, weights = SimpleCubeSpectraCombiner.combine(subcube, subwhite,
                                                          combine_method=combine_method, weighter=weight_method)
        if spec is None or weights is None:
            return None
        spec.primary_header["RA_OBJ"] = ra
        spec.primary_header["DEC_OBJ"] = dec
        spec.primary_header["ID_OBJ"] = spectrum_id

        setattr(spec, "white_cutout", np.nansum(subcube.data, axis=0))
        setattr(spec, "mask_cutout", subcube.data.mask[0].astype(int))
        setattr(spec, "weight_cutout", weights)
        return spec
