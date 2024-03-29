import setuptools

#with open("README.md", "r", encoding="utf-8") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="CubeExtractor",
    version="0.0.1",
    author="Joaquin Hernandez",
    author_email="joaquin.hernandezg@uc.cl",
    description="A code to perform spectral extraction on MUSE cubes",
    #long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joaquinhernandezg/CubeExtractor",
    project_urls={
        "Bug Tracker": "https://github.com/joaquinhernandezg/CubeExtractor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Scientific/Engineering :: Astrophysics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    # add sewpy
    install_requires=['numpy', 'scipy', 'astropy>=5.2.1',
                      'photutils>=1.8', 'tqdm', 'mpdaf',
                      'linetools',
                      #'sewpy @ git+ssh://git@github.com:megalut/sewpy.git#egg=sewpy'
                      ],
    entry_points={
                        'console_scripts': [
                                'cube_extract=CubeExtractor.bin.cube_extract_inline:ExtractSpectraFromCubeInlineScript.entry_point',
                                'cube_extract_config=CubeExtractor.bin.cube_extract:ExtractSpectra.entry_point',
                                'cube_plot_apertures=CubeExtractor.bin.plot_apertures:PlotAperturesScript.entry_point',
                                'cube_make_white=CubeExtractor.bin.make_white_image:MakeWhiteImageScript.entry_point',
                                'cube_gen_config=CubeExtractor.bin.gen_config:MakeConfig.entry_point'
                               ]
                }
)