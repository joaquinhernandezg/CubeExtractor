from .scriptbase import ScriptBase, str2bool
from CubeExtractor.spectra.extractor import (CircularApertureExtractor,
                                        EllipticalApertureExtractor,
                                        MaskExtractor)
from CubeExtractor.utils.batch_extract import extract_batch_spectra
from CubeExtractor.utils.utils import write_extraction_data
import argparse
import os

from astropy.table import Table
from astropy.io import fits



import logging
logging.basicConfig(level = logging.INFO)


class ExtractSpectraFromCubeInlineScript(ScriptBase):

    @classmethod
    def get_parser(cls, width=None):
        parser = super().get_parser(description='Convolves a set of images based on a set of PSFs.', width=width)


        parser.add_argument("--cube_filename", type=str, help="Cube filename")
        parser.add_argument("--white_image_filename", type=str, help="White image of the cube")

        parser.add_argument("--sextractor_catalog_filename", type=str, help="Sextractor catalog filename")
        parser.add_argument("--skip_exceptions", type=str2bool, help="If True, skips exceptions and just logs them")

        parser.add_argument("--aperture_type", type=str, default="elliptical", help="Aperture type")
        parser.add_argument("--combine_method", type=str, default="sum", help="Combination function")
        parser.add_argument("--weight_method", type=str, default=None, help="Weighting function")
        parser.add_argument("--segmentation_mask", type=str, default=None, help="segmentation mask")

        parser.add_argument("--redmonster_spectra_outdir", type=str, default=None, help="Output redmonster spectra")
        parser.add_argument("--marz_spectra_outfile", type=str, default=False, help="Output marz spectra")
        parser.add_argument("--linetools_spectra_dir", type=str, default=False, help="Output linetools spectra")

        parser.add_argument("--output_subcubes", type=bool, default=False, help="Output subcubes")
        parser.add_argument("--output_masks", type=bool, default=False, help="Output masks")
        parser.add_argument("--output_weights", type=bool, default=False, help="Output masks")

        parser.add_argument("--ra_column", type=str, default="ALPHA_J2000", help="RA column")
        parser.add_argument("--dec_column", type=str, default="DELTA_J2000", help="RA column")
        parser.add_argument("--id_column", type=str, default="NUMBER", help="ID column")
        parser.add_argument("--only_first_n", type=int, default=-1, help="First n ids to extract")

        parser.add_argument("--out_cutouts_dir", type=str, default=None, help="cutouts directory")
        parser.add_argument("--cut_edges_segmentation", type=int, default=10, help="trim edges of segmentation mask")


        parser.add_argument("--overwrite_all", type=str2bool, default=False, help="Overwrite all files")

        return parser


    @staticmethod
    def main(args):

        # basic input verification

        # checks if the cube exists
        if not os.path.exists(args.cube_filename):
            raise ValueError("Cube filename {} does not exist".format(args.cube_filename))
        if not os.path.exists(args.white_image_filename):
            raise ValueError("White image filename {} does not exist".format(args.cube_filename))
        # checks if the catalog exists
        if not os.path.exists(args.sextractor_catalog_filename):
            raise ValueError("Sextractor catalog filename {} does not exist".format(args.sextractor_catalog_filename))
        # verify sextractor spectra is .fits file
        if not args.sextractor_catalog_filename.endswith(".fits"):
            raise ValueError("Sextractor catalog filename {} is not a .fits file".format(args.sextractor_catalog_filename))

        # reads the sources catalog
        logging.info(f"Reading catalog: {args.sextractor_catalog_filename}")
        catalog = Table.read(args.sextractor_catalog_filename)

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

        # reads the cube
        logging.info(f"Reading Cube: {args.cube_filename}")

        # if the white image is passed, plot the segmentation mask and/or the
        # defines apertures over the white image
        # extract the spectra
        spectra = extract_batch_spectra(cube_filename=args.cube_filename, white_filename=args.white_image_filename,
                                        catalog_filename=args.sextractor_catalog_filename,
                                        aperture_extractor=aperture_extractor, combine_method=args.combine_method,
                                        weight_method=args.weight_method, ra_column=args.ra_column,
                                        dec_column=args.dec_column, id_column=args.id_column,
                                        segmentation_mask_filename=args.segmentation_mask,
                                        skip_exceptions=args.skip_exceptions, extract_only_n=args.only_first_n,)

        write_extraction_data(spectra, out_cutous_dir=args.out_cutouts_dir, marz_table_filename=args.marz_spectra_outfile,
                              linetools_outdir=args.linetools_spectra_dir, redmonster_outdir=args.redmonster_spectra_outdir,
                              overwrite=args.overwrite_all)
