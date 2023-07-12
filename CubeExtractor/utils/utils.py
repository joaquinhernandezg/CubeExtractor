from mpdaf.obj import Cube, Spectrum, Image
import numpy as np

def make_white_image(cube, out_filename=None, mask_nans=True, wave_min=None, wave_max=None):
    if isinstance(cube, str):
        cube = Cube(cube)
    if not isinstance(cube, Cube):
        raise ValueError("cube must be a path to a cube or a Cube instance")

    if mask_nans:
        cube.data.mask = np.isnan(cube.data)
        cube.var.mask = np.isnan(cube.var)

    #TODO: add the cases where wave_min or wave_max are None, take them as the min and max of the cube
    if wave_min is not None and wave_max is not None:
        cube = cube.select_lambda(wave_min, wave_max)

    white = cube.sum(axis=0)

    if isinstance(out_filename, str):
        white.write(out_filename )
    return white



