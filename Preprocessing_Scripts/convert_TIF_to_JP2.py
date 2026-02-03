# convert_TIF_to_JP2.py
# Converts a TIF to a JP2 file to compress for uploads
# Used when image tiles are downloaded as full resolution TIF files
# User must set the input and output directories

import os
import rasterio
from rasterio import shutil as rio_shutil

# Set the input and output directories
input_folder = r"REPLACE-WITH-PATH-TO-INPUT-FOLDER"
output_folder = r"REPLACE-WITH-PATH-TO-OUTPUT-FOLDER"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate through all files in the input folder
for file_name in os.listdir(input_folder):
    # Check for TIF or TIFF files
    if file_name.lower().endswith((".tif", ".tiff")):
        tif_path = os.path.join(input_folder, file_name)
        # Build name and path for output JP2 file
        jp2_name = os.path.splitext(file_name)[0] + ".jp2"
        jp2_path = os.path.join(output_folder, jp2_name)

        # Open the TIF file and convert it to a JP2 file
        with rasterio.open(tif_path) as src:
            rio_shutil.copy(src, jp2_path, driver="JP2OpenJPEG", quality=25)

        print(f"Converted: {tif_path} -> {jp2_path}")

print("Processing complete!")