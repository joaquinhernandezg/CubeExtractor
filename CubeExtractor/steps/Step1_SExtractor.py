import sewpy
import os
def run_sex(workdir, sexpath, image_path, config_name, params_name, catalog_name,
            segmentation_image="segmentation.fits", apertures_image="apertures.fits",
            make_segm=True, make_apertures=True,
            data_ext=1, var_ext=2, use_var=False):

    catalog_name = os.path.join(workdir, catalog_name)
    checkimage_type = []
    checkimage_name = []
    if make_apertures:
        checkimage_type.append("APERTURES")
        checkimage_name.append(os.path.join(workdir, apertures_image))
    if make_segm:
        checkimage_type.append("SEGMENTATION")
        checkimage_name.append(os.path.join(workdir, segmentation_image))


    weight_type = "NONE"
    weight_image = "NONE"
    if use_var:
        weight_type = "MAP_VAR"
        weight_image = image_path+f"[{var_ext}]"



    sew = sewpy.SEW(
        config={
                "PARAMETERS_NAME": params_name,
                "CHECKIMAGE_TYPE": ",".join(checkimage_type),
                "CHECKIMAGE_NAME": ",".join(checkimage_name),
                "WEIGHT_TYPE": weight_type,
                "WEIGHT_IMAGE": weight_image,
                },

        configfilepath=config_name,
        workdir=workdir,
        sexpath=sexpath,
        )
    out_dict = sew(imgfilepath=image_path,
                   returncat=True)
    table = out_dict["table"]
    table.write(catalog_name, overwrite=True)
    return