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



## Command-line Scripts

All the provided command-line scripts can be run with the option `-h` to print a description of the script and its parameters.

### White image creation
`
cube_make_white --cube_filename cube.fits --white_image_filename white.fits
`

### Plot Apertures
`
cube_plot_apertures --white_image_filename white.fits --out_filename apertures.pdf --aperture type segmentation --segmentation_mask segmentation.fits
`


