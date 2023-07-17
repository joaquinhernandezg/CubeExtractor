from .scriptbase import ScriptBase, str2bool
from CubeExtractor.utils.config import make_default_config

import os



import logging
logging.basicConfig(level = logging.INFO)

class MakeConfig(ScriptBase):

    @classmethod
    def get_parser(cls, width=None):
        parser = super().get_parser(description='Creates a default configurationf file', width=width)
        parser.add_argument("--config_filename", type=str, help="Name of the configuration file to create", default="extract.ini")
        parser.add_argument("--overwrite", type=str2bool, default=False, help="Overwrite")
        return parser


    @staticmethod
    def main(args):
        if os.path.exists(args.config_filename) and not args.overwrite:
            raise ValueError("Config file {} already exists".format(args.config_filename))

        config = make_default_config()
        config.write(args.config_filename)



