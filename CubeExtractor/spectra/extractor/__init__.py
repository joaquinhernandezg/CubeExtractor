from .mask_extractor import MaskExtractor
from .aperture_extractor import (CircularApertureExtractor,
                                EllipticalApertureExtractor)

def get_aperture_extractor(aperture_type):
    """
    Returns the aperture extractor class for the given aperture type.
    """
    # defines the handler for each aperture type
    if aperture_type == "elliptical":
        aperture_extractor = EllipticalApertureExtractor
    elif aperture_type == "circular":
        aperture_extractor = CircularApertureExtractor
    elif aperture_type == "segmentation":
        aperture_extractor = MaskExtractor
    else:
        raise ValueError("Aperture type {} is not supported".format(aperture_type))
    return aperture_extractor