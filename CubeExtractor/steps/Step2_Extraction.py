



spectra = extract_batch_spectra(cube_filename=args.cube_filename, white_filename=args.white_image_filename,
                                        catalog_filename=args.sextractor_catalog_filename,
                                        aperture_extractor=aperture_extractor, combine_method=args.combine_method,
                                        weight_method=args.weight_method, ra_column=args.ra_column,
                                        dec_column=args.dec_column, id_column=args.id_column,
                                        segmentation_mask_filename=args.segmentation_mask,
                                        skip_exceptions=args.skip_exceptions,)

write_extraction_data(spectra, out_cutous_dir=args.out_cutouts_dir, marz_table_filename=args.marz_spectra_outfile,
                        linetools_outdir=args.linetools_spectra_dir, redmonster_outdir=args.redmonster_spectra_outdir,
                        overwrite=args.overwrite_all)