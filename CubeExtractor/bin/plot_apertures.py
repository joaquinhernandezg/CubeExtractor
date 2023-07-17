from .scriptbase import ScriptBase

from .scriptbase import ScriptBase, str2bool
from CubeExtractor.utils.plot import plot_apertures
from CubeExtractor.spectra.extractor import (CircularApertureExtractor, EllipticalApertureExtractor, MaskExtractor)
from astropy.table import Table
from mpdaf.obj import Image
import argparse
import os
from astropy.io import fits



import logging
logging.basicConfig(level = logging.INFO)


class PlotAperturesScript(ScriptBase):
    @classmethod
    def get_parser(cls, width=None):
        parser = super().get_parser(description='Convolves a set of images based on a set of PSFs.', width=width)


        parser.add_argument("--white_image_filename", type=str, help="White image of the cube")
        parser.add_argument("--catalog", type=str, help="Sextractor catalog filename")
        parser.add_argument("--out_filename", type=str, default=None, help="filename of the plot if saved")

        parser.add_argument("--aperture_type", type=str, default="elliptical", help="Aperture type")
        parser.add_argument("--segmentation_mask", type=str, default=None, help="segmentation mask")



        parser.add_argument("--ra_column", type=str, default="ALPHA_J2000", help="RA column")
        parser.add_argument("--dec_column", type=str, default="DELTA_J2000", help="RA column")
        parser.add_argument("--id_column", type=str, default="NUMBER", help="ID column")


        parser.add_argument("--overwrite", type=str2bool, default=False, help="Overwrite all files")

        return parser

    @staticmethod
    def main(args):

        # basic input verification

        if not os.path.exists(args.white_image_filename):
            raise ValueError("White image filename {} do not exists".format(args.white_image_filename))

        # defines the handler for each aperture type
        if args.aperture_type == "elliptical":
            aperture_extractor = EllipticalApertureExtractor
        elif args.aperture_type == "circular":
            aperture_extractor = CircularApertureExtractor
        elif args.aperture_type == "segmentation":
            aperture_extractor = MaskExtractor
        else:
            raise ValueError("Aperture type {} is not supported".format(args.aperture_type))
        logging.info(f"Using aperture: {args.aperture_type}")

        white = Image(args.white_image_filename)
        catalog = Table.read(args.sextractor_catalog_filename)
        segmentation_mask = fits.getdata(args.segmentation_mask) if args.segmentation_mask else None

        #TODO: add colors to the apertures
        fig, ax = plot_apertures(white, catalog, ra_column=args.ra_column, dec_column=args.dec_column,
                                 id_column=args.id_column, aperture_extractor=aperture_extractor,
                                 segmentation_mask=segmentation_mask)
        if args.out_filename:
            fig.savefig(args.out_filename)



