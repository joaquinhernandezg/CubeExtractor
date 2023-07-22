from .scriptbase import ScriptBase, str2bool
from CubeExtractor.utils.config import ReadConfig
import configparser
from CubeExtractor.steps import RunSteps

import os

import logging
logging.basicConfig(level = logging.INFO)


class ExtractSpectra(ScriptBase):

    @classmethod
    def get_parser(cls, width=None):
        parser = super().get_parser(description='Convolves a set of images based on a set of PSFs.', width=width)


        parser.add_argument("config_file", type=str, help="Config file")

        return parser


    @staticmethod
    def main(args):

        # basic input verification

        # checks if the cube exists
        if not os.path.exists(args.config_file):
            raise ValueError("Config file {} does not exist".format(args.config_file))

        config = ReadConfig(args.config_file).config
        RunSteps(config)


        # Veryfy inputs and create dirs









