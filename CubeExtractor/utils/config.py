import configparser
import os
from astropy.table import Table


def make_default_config():
    config = configparser.ConfigParser()
    config["CONFIG"] = {"SEX_PATH": "/bin/sex"}

    config["INPUT"] = {"CUBE": "",
                       "WHITE_IMAGE": "",
                       "CUBE_DATA_EXT": "0",
                       "CUBE_VAR_EXT": "1",
                       "WHITE_DATA_EXT": "0",
                       "WHITE_VAR_EXT": "1"}

    config["WORKDIR"] = {"MAIN": "CubeExtraction",
                         "SEXTRACTOR": "sextractor",
                         "SPECTRA": "spectra",
                         "CUTOUTS": "cutouts"}

    config["SEXTRACTOR"] = {"RUN": "yes",
                            "CONFIG_NAME": "default.sex",
                            "PARAMS_NAME": "default.param",
                            "CATALOG_NAME": "cat.fits",
                            "SEGMENTATION_IMAGE": "seg.fits",
                            "APERTURES_IMAGE": "aper.fits",
                            "MAKE_SEGMASK": "yes",
                            "MAKE_APERTURES": "yes",
                            "USE_VARMAP": "no"}

    config["EXTRACTION"] = {"RUN": "yes",
                            "APERTURE": "elliptical",
                            "COMBINE": "sum",
                            "WEIGHT": "none",
                            "RA_COLUMN": "ALPHA_J2000",
                            "DEC_COLUMN": "DELTA_J2000",
                            "A_COLUMN": "A_WORLD",
                            "B_COLUMN": "B_WORLD",
                            "THETA_COLUMN": "THETA_WORLD"
                            }
    config["OUTPUT"] = {"CUTOUTS": "yes",
                        "MARZ": "yes",
                        "LINETOOLS": "yes",
                        "REDMONSTER": "yes",
                        "MARZ_NAME": "marz_table.fits",
                        "LINETOOLS_DIR": "linetools_spectra",
                        "REDMONSTER_DIR": "redmonster_spectra",
                        "OVERWRITE": "yes"}
    config["DEBUG"] = {"SKIP_EXTRACTION_ERRORS": "yes",
                       "EXTRACT_FIRST_N": "-1"}
    config["PLOT"] = {"PlotApertures": "yes"}

    return config

class ReadConfig:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def check_all(self):
        self.check_config()
        self.check_input()
        self.check_extraction()

    def check_config(self):
        SEX_PATH = self.config["CONFIG"]["SEX_PATH"]
        assert os.path.exists(SEX_PATH)

    def check_input(self):
        cube = self.config["INPUT"]["CUBE"]
        white = self.config["INPUT"]["WHITE_IMAGE"]
        cube_data_ext = self.config["INPUT"]["CUBE_DATA_EXT"]
        cube_var_ext = self.config["INPUT"]["CUBE_VAR_EXT"]
        white_data_ext = self.config["INPUT"]["WHITE_DATA_EXT"]
        white_var_ext = self.config["INPUT"]["WHITE_VAR_EXT"]

        assert os.path.exists(cube)
        assert os.path.exists(white)
        assert cube_data_ext.isdigit()
        assert cube_var_ext.isdigit()
        assert white_data_ext.isdigit()
        assert white_var_ext.isdigit()

    def check_sextractor(self):
        run = self.config["SEXTRACTOR"]["RUN"]
        config_name = self.config["SEXTRACTOR"]["CONFIG_NAME"]
        params_name = self.config["SEXTRACTOR"]["PARAMS_NAME"]
        catalog_name = self.config["SEXTRACTOR"]["CATALOG_NAME"]
        segmentation_image = self.config["SEXTRACTOR"]["SEGMENTATION_IMAGE"]
        aperture_image = self.config["SEXTRACTOR"]["APERTURES_IMAGE"]
        make_segm = self.config["SEXTRACTOR"]["MAKE_SEGMASK"]
        make_apertures = self.config["SEXTRACTOR"]["MAKE_APERTURES"]
        use_varmap = self.config["SEXTRACTOR"]["USE_VARMAP"]

        assert run in ["yes", "no"]
        if run == "no":
            return
        assert os.path.exists(config_name)
        assert os.path.exists(params_name)
        assert os.path.exists(catalog_name)
        assert segmentation_image.endswith(".fits")
        assert aperture_image.endswith(".fits")
        assert make_segm in ["yes", "no"]
        assert make_apertures in ["yes", "no"]
        assert use_varmap in ["yes", "no"]

    def check_extraction(self):
        run = self.config["EXTRACTION"]["RUN"]
        aperture = self.config["EXTRACTION"]["APERTURE"]
        combine = self.config["EXTRACTION"]["COMBINE"]
        weight = self.config["EXTRACTION"]["WEIGHT"]
        ra_column = self.config["EXTRACTION"]["RA_COLUMN"]
        dec_column = self.config["EXTRACTION"]["DEC_COLUMN"]
        a_column = self.config["EXTRACTION"]["A_COLUMN"]
        b_column = self.config["EXTRACTION"]["B_COLUMN"]
        theta_column = self.config["EXTRACTION"]["THETA_COLUMN"]

        assert run in ["yes", "no"]
        assert aperture in ["segmentation", "elliptical", "circular"]
        assert combine in ["sum", "mean", "median"]
        assert weight in ["none"]







