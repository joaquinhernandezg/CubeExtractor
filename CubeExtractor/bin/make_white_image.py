from .scriptbase import ScriptBase, str2bool
from CubeExtractor.utils.utils import make_white_image

import argparse
import os

from astropy.table import Table
from astropy.io import fits



import logging
logging.basicConfig(level = logging.INFO)

class MakeWhiteImageScript(ScriptBase):

    @classmethod
    def get_parser(cls, width=None):
        parser = super().get_parser(description='Creates a white image collapsing a Cube', width=width)


        parser.add_argument("--cube_filename", type=str, help="Cube filename")
        parser.add_argument("--white_image_filename", type=str, help="White image of the cube")
        parser.add_argument("--wave_min", default=None, type=float, help="Minimun wavelength in Angstroms")
        parser.add_argument("--wave_max", default=None, type=float, help="Maximum wavelength in Angstroms")
        parser.add_argument("--overwrite", type=str2bool, default=False, help="Overwrite all files")

        return parser


    @staticmethod
    def main(args):

        # basic input verification

        # checks if the cube exists
        if not os.path.exists(args.cube_filename):
            raise ValueError("Cube filename {} does not exist".format(args.cube_filename))

        if os.path.exists(args.white_image_filename) and not args.overwritex:
            raise ValueError("White image filename {} already exists".format(args.white_image_filename))

        make_white_image(args.cube_filename, args.white_image_filename,
                         mask_nans=True, wave_min=args.wave_min,
                         wave_max=args.wave_max)



