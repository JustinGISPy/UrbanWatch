# Modification of original UrbanWatch script to use rasterio instead of GDAL
# Transfers projection information from the original images to the UrbanWatch output images
# Input images and LC Result images MUST have the same name
# User must set the input, lc_result, and output directories

import os
import glob
import rasterio

def get_filename_without_extension(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

def create_file_mapping(input_files, result_files):
    input_dict = {get_filename_without_extension(f): f for f in input_files}
    result_dict = {get_filename_without_extension(f): f for f in result_files}
    return [(input_dict[k], result_dict[k]) for k in input_dict if k in result_dict]

def process_projection_transfer(input_dir, result_dir, output_dir):
    """
    Main processing function to transfer projections from input images to lc_result images
    """
    input_images = (
        glob.glob(os.path.join(input_dir, '*.tif')) +
        glob.glob(os.path.join(input_dir, '*.TIF'))
    )

    lc_results = (
        glob.glob(os.path.join(result_dir, '*.tif')) +
        glob.glob(os.path.join(result_dir, '*.TIF'))
    )

    # Stop if input directory does not contain TIF files
    if not input_images:
        print(f"No TIFF files found in input directory: {input_dir}")
        return

    # Stop if lc_result directory does not contain TIF files
    if not lc_results:
        print(f"No TIFF files found in result directory: {result_dir}")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create file mapping based on matching filenames
    matched_pairs = create_file_mapping(input_images, lc_results)

    # Stop if no matching file pairs are found
    if not matched_pairs:
        print("No matching file pairs found.")
        return

    # Process each matched file pair
    print(f"Processing {len(matched_pairs)} raster pairs...\n")
    for src_path, res_path in matched_pairs:
        base_name = get_filename_without_extension(src_path)
        output_file = os.path.join(output_dir, f"{base_name}_LC.tif")

        print(f"Processing: {base_name}")

        with rasterio.open(src_path) as src_ds, rasterio.open(res_path) as res_ds:

            ### SAFETY CHECK 
            if (src_ds.width != res_ds.width) or (src_ds.height != res_ds.height):
                raise ValueError(
                    f"Dimension mismatch for {base_name}:\n"
                    f"  Source: {src_ds.width} x {src_ds.height}\n"
                    f"  Result: {res_ds.width} x {res_ds.height}\n"
                    f"Cannot safely assign spatial reference."
                )

            # Read result data
            res_data = res_ds.read()

            # Write output using source spatial reference
            with rasterio.open(
                output_file,
                'w',
                driver='GTiff',
                height=src_ds.height,
                width=src_ds.width,
                count=res_ds.count,
                dtype=res_data.dtype,
                crs=src_ds.crs,
                transform=src_ds.transform
            ) as dst:
                dst.write(res_data)

        print(f"Processed: {base_name}_LC.tif\n")

    print("All rasters processed successfully.")

def main():
    # Set the input, lc_result, and output directories
    input_folder = r"REPLACE-WITH-PATH-TO-INPUT-FOLDER"
    lc_result_folder = r"REPLACE-WITH-PATH-TO-LC_RESULT-FOLDER"
    output_folder = r"REPLACE-WITH-PATH-TO-OUTPUT-FOLDER"

    process_projection_transfer(input_folder, lc_result_folder, output_folder)

if __name__ == '__main__':
    main()