from .Step1_SExtractor import run_sex
import os

class RunSteps:
    def __init__(self, config):
        self.config = config

    def step1_SExtractor(self):
        """
        Run SExtractor on the input images.
        """
        main_workdir = self.config["WORKDIR"]["MAIN"]
        sex_workdir = self.config["WORKDIR"]["SEXTRACTOR"]

        sex_workdir = os.path.join(main_workdir, sex_workdir)

        sex_path = self.config["CONFIG_PATH"]

        config_name = self.config["SEXTRACTOR"]["CONFIG_NAME"]
        params_name = self.config["SEXTRACTOR"]["PARAMS_NAME"]
        catalog_name = self.config["SEXTRACTOR"]["CATALOG_NAME"]
        segmentation_image = self.config["SEXTRACTOR"]["SEGMENTATION_IMAGE"]
        apertures_image = self.config["SEXTRACTOR"]["APERTURES_IMAGE"]
        make_segm = self.config["SEXTRACTOR"]["MAKE_SEGMASK"]
        make_aper = self.config["SEXTRACTOR"]["MAKE_APERTURES"]
        use_varmap = self.config["SEXTRACTOR"]["USE_VARMAP"]

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
            make_apertures=make_aper,
            data_ext=data_ext,
            var_ext=var_ext,
            use_var=use_varmap,
        )


    def step2_Extraction(self):
        pass