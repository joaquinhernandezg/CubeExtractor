# CubeExtractor
A code for extracting spectra in IFU data.
Its is designed to use catalogs and segmentation images from SExtractor to do extraction of spectra in MUSE cubes, incorporating different types of apertures and spaxel weighting.

## SExtractor
The first step is to run SExtractor on a white image of the cube. Make sure to include the NUMBER, ALPHA_J2000, DELTA_J2000, A_WORLD, B_WORLD, and THETA_WORLD in your default.param file.

The provided command-line script "cube_make_white" creates a white image collapsing the fluxes and variances.

The idea is that you run SExtractor on this white image taking care of detecting your sources of interest. In the case you want to use the variance extension of the whit white image as a MAP_RMS SExtractor image, you can pass the VAR extension in the *default.sex* as

```
WEIGHT_TYPE VAR
WEIGHT_IMAGE white_image.fits[2]
```

or directly in the command line as

`
sex white_image.fits[1] -c default.sex -WEIGHT_TYPE MAP_VAR -WEIGHT_IMAGE white_image.fits[2]
`

Explanation: The white image we created has two extensions, one contains the fluxes, and other the variances. If we run SExtractor directly on the image, it will try to detect sources on all the extensions. By adding "[1]" at the end of the filename, we tell it to detect sources just on the first extension. Then for the weights, we tell that the seconda extension "[2]" has the variances. We might as well pass a diferent filename, but in out case it is just in other extension of the same file.

Detection parameters in the *default.sex* have to be manually tuned in order to detect the sources you want to. Going for fainter sources makes SExtractor detect spurous sources in the edges of the cubes or in the "stripes" produced by the CDDs. Using the variance for the source detection should reduce the number of this kind if detections, while keeping the real sources.

As a rule of thumb, always output the apertures, segmentation, and background images. If your cube present severe "stripes" from the MUSE CCDs, try playing with the background parameters, until you get see the background checkimage correctly estimates it (in order to substract it later). Constantly check you aperture checkimage in order to verify your sources of interest are being detected. Also, checking the segmentation checkimage is useful to check is the deblending is working properly, this is important, we use the segmentation image for extraction of spectra.

## Extraction of spectra
Once you obtained an extraction that is appropiated for your science purposes you can use the SExtractor catalog and segmentation images to extract spectra on the cubes.

The command `cube_extract` does the extraction.

Usage

`
cube_extract --cube_filename cube.fits \
             --white_image_filename white.fits \
             --sextractor_catalog_filename sources.fits \
             --aperture_type segmentation \
             --segmentation_mask segmentation.fits \
             --weight_method snr\
             --redmonster_spectra_outdir redmonster \
             --marz_spectra_outfile  marz.fits\
             --linetools_spectra_dir linetools\
`

In this caase, we are running the extraction on cube.fits, where sources were detected on white.fits, producing a catalog sources.fits and segmentation image segmentation.fits. Extraction is performed using segmentation masks, from the file segmentation.fits. Spectra will be extracted for each segmentation mask, weighting by signal-to-noise. Spectra are saved in redmonster format to the "/redmonster" directory, in linetools format to the "/linestools" directory, and a marz table is saved as *marz.fits*.

Linetools spectra can be opened with the `linetools` python library and with its `lt_xspec` command-line script.

Marz table can be directly uploaded to the Marz webpage to do a session of (very fun) redshifting (http://samreay.github.io/Marz/#/overview). Although I personally recommend to use a local forked version with more templates.




## Command-line Scripts

All the provided command-line scripts can be run with the option `-h` to print a description of the script and its parameters.

### White image creation
`
$ cube_make_white --cube_filename cube.fits --white_image_filename white.fits
`

### Plot Apertures
`
$ cube_plot_apertures --white_image_filename white.fits --out_filename apertures.pdf --aperture type segmentation --segmentation_mask segmentation.fits
`



## The configuration file

The command

`
$ cube_gen_config
`

generates the configuration file that stores the variables for doing the detection and extraction of sources in a given cube. It generates a file containing several variables.

### [CONFIG] section
#### SEX_PATH
Defines the path to the SExtractor exectutable. When the configuration file is generates with the command  `$ cube_gen_config` it is automatically set. Otherwise, you can search it in your path by executing `$ which sex`, and copy-paste the returned path.

### [INPUT] section
#### CUBE
The filename of the IFU datacube where the software will be run. It should have defined a WCS, and a DATA and VAR extensions.

#### WHITE_IMAGE
White image created by collapsing *CUBE* along the spectral axis. It is used as detection image by SExtractor. Should be constructed by running the  `$ cube_make_white` command.

#### CUBE_DATA_EXT
Extension where the fluxes are stored in the IFU cube.

#### CUBE_VAR_EXT
Extension where the variances are stored in the IFU cube.

#### WHITE_DATA_EXT
Extension where the fluxes are stored in the white image.

#### WHITE_VAR_EXT
Extension where the variances are stored in the white image.


### [WORDIR] section
Here are defined the directories where the input and output data are/will be stored.

#### MAIN
All the output data products will be stored in "./*MAIN*"

#### SEXTRACTOR
SExtractor output data will be stored in "./*MAIN*/*SEXTRACTOR*"

#### SPECTRA
Extracted spectra data will be stored in "./*MAIN*/*SEXTRACTOR*/\*"

#### CUTOUTS
Output files for verifying extraction will be stored in "./*MAIN*/*CUTOUTS*/\*"


### [SExtractor] section

This sections defines the necessary input files to run SExtractor on the detection image.

#### RUN
Run the source detection (yes/no). If the sofware is run for the first time, this need to be set to *yes* in order to create the input for running the extraction. If you are satisfied with the source detection, you can set this option to *no* and continue with the other steps.

#### CONFIG_NAME
The SExtractor configuration file, usually called *default.sex*. All the parameters regarding source detection, deblending, etc., are determined by this files, and should be tuned in an iterative way.

#### PARAMS_NAME
The SExtractor parameters file. All the paramters that SExtractor will measure for the output catalogue are defined in this file. Minimun parameters are required for this software to run. NUMBER, ALPHA_J2000, DELTA_J2000, FLUX_RADIUS, A_WORLD, B_WORLD, THETA_WORLD.

#### CATALOG_NAME
Name of the catalog output by SExtractor. It is used later for the spectral extraction.

#### SEGMENTATION_IMAGE
Name of the output segmentation checkimage created by SExtractor. It can be used for spectral extraction in the *segmentation* extraction model. You can also use this image to check the source detection and debleding.

#### APERTURES_IMAGE
Name of the output apertures checkimage created by SExtractor. You can also use this image to check the source detection and debleding. You need to ask a flux/magnitude measurement in *PARAMS_NAME* in order for SExtractor to draw the apertures.

#### MAKE_SEGMASK








