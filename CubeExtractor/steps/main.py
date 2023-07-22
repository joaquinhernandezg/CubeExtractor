from .Step1_SExtractor import run_sex
import os
from astropy.table import Table
from ..spectra.extractor import get_aperture_extractor
import logging
from ..utils.batch_extract import extract_batch_spectra
from ..utils.utils import write_extraction_data

class RunSteps:
    def __init__(self, config):
        self.config = config
        if self.config["SEXTRACTOR"].getboolean("RUN"):
            self.step1_SExtractor()
        self.step2_Extraction()

    def step1_SExtractor(self):
        """
        Run SExtractor on the input images.
        """
        main_workdir = self.config["WORKDIR"]["MAIN"]
        sex_workdir = self.config["WORKDIR"]["SEXTRACTOR"]

        sex_workdir = os.path.join(main_workdir, sex_workdir)

        sex_path = self.config["CONFIG"]["SEX_PATH"]

        config_name = self.config["SEXTRACTOR"]["CONFIG_NAME"]
        params_name = self.config["SEXTRACTOR"]["PARAMS_NAME"]
        catalog_name = self.config["SEXTRACTOR"]["CATALOG_NAME"]
        segmentation_image = self.config["SEXTRACTOR"]["SEGMENTATION_IMAGE"]
        apertures_image = self.config["SEXTRACTOR"]["APERTURES_IMAGE"]
        make_segm = self.config["SEXTRACTOR"]["MAKE_SEGMASK"]
        make_aper = self.config["SEXTRACTOR"]["MAKE_APERTURES"]
        use_varmap = self.config["SEXTRACTOR"].getboolean("USE_VARMAP")

        image_path = self.config["INPUT"]["WHITE_IMAGE"]
        data_ext = self.config["INPUT"]["WHITE_DATA_EXT"]
        var_ext = self.config["INPUT"]["WHITE_VAR_EXT"]


        run_sex(
            workdir=sex_workdir,
            sexpath=sex_path,
            image_path=image_path,
            config_name=config_name,
            params_name=params_name,
            catalog_name=catalog_name,
            make_segm=make_segm,
            segmentation_image=segmentation_image,
            apertures_image=apertures_image,
            make_apertures=make_aper,
            data_ext=data_ext,
            var_ext=var_ext,
            use_var=use_varmap,
        )


    def step2_Extraction(self):
        main_workdir = self.config["WORKDIR"]["MAIN"]
        sex_workdir = self.config["WORKDIR"]["SEXTRACTOR"]

        sex_workdir = os.path.join(main_workdir, sex_workdir)
        catalog_name = self.config["SEXTRACTOR"]["CATALOG_NAME"]
        catalog_name = os.path.join(sex_workdir, catalog_name)

        cube_filename = self.config["INPUT"]["CUBE"]
        white_filename = self.config["INPUT"]["WHITE_IMAGE"]
        weight_method = self.config["EXTRACTION"]["WEIGHT"]
        segmentation_mask = self.config["SEXTRACTOR"]["SEGMENTATION_IMAGE"]
        segmentation_mask = os.path.join(sex_workdir, segmentation_mask)
        skip_exceptions = self.config["DEBUG"].getboolean("SKIP_EXTRACTION_ERRORS")
        combine_method = self.config["EXTRACTION"]["COMBINE"]
        ra_column = self.config["EXTRACTION"]["RA_COLUMN"]
        dec_column = self.config["EXTRACTION"]["DEC_COLUMN"]
        theta_column = self.config["EXTRACTION"]["THETA_COLUMN"]
        a_column = self.config["EXTRACTION"]["A_COLUMN"]
        b_column = self.config["EXTRACTION"]["B_COLUMN"]
        extract_only_n = int(self.config["DEBUG"]["EXTRACT_FIRST_N"])

        aperture_type = self.config["EXTRACTION"]["APERTURE"]

        do_cutouts = self.config["OUTPUT"].getboolean("CUTOUTS")
        do_marz = self.config["OUTPUT"].getboolean("MARZ")
        do_linetools = self.config["OUTPUT"].getboolean("LINETOOLS")
        do_redmonster = self.config["OUTPUT"].getboolean("REDMONSTER")

        out_cutouts_dir = self.config["OUTPUT"]["CUTOUTS_DIR"]
        out_cutouts_dir = os.path.join(main_workdir, out_cutouts_dir)
        if not do_cutouts:
            out_cutouts_dir = None
        marz_name = self.config["OUTPUT"]["MARZ_NAME"]
        marz_name = os.path.join(main_workdir, marz_name)
        if not do_marz:
            marz_name = None
        linetools_dir = self.config["OUTPUT"]["LINETOOLS_DIR"]
        linetools_dir = os.path.join(main_workdir, linetools_dir)
        if not do_linetools:
            linetools_dir = None
        redmonster_dir = self.config["OUTPUT"]["REDMONSTER_DIR"]
        redmonster_dir = os.path.join(main_workdir, redmonster_dir)
        if not do_redmonster:
            redmonster_dir = None
        overwrite = self.config["OUTPUT"].getboolean("OVERWRITE")

        # defines the handler for each aperture type
        aperture_extractor = get_aperture_extractor(aperture_type)

        logging.info(f"Using aperture: {aperture_type}")

        # reads the cube
        logging.info(f"Reading Cube: {cube_filename}")

        # if the white image is passed, plot the segmentation mask and/or the
        # defines apertures over the white image
        # extract the spectra

        spectra = extract_batch_spectra(cube_filename=cube_filename, white_filename=white_filename,
                                        catalog_filename=catalog_name,
                                        aperture_extractor=aperture_extractor, combine_method=combine_method,
                                        weight_method=weight_method, ra_column=ra_column,
                                        dec_column=dec_column, id_column="NUMBER",
                                        segmentation_mask_filename=segmentation_mask,
                                        skip_exceptions=skip_exceptions, extract_only_n=extract_only_n)


        write_extraction_data(spectra, out_cutous_dir=out_cutouts_dir, marz_table_filename=marz_name,
                              linetools_outdir=linetools_dir, redmonster_outdir=redmonster_dir,
                              overwrite=overwrite)

        pass