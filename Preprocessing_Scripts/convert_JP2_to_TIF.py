# convert_JP2_to_TIF.py
# Converts a compressed JP2 image file to a TIF file
# Used when image tiles are downloaded as .jp2 files
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
    # Check for JP2 files
    if file_name.lower().endswith(".jp2"):
        jp2_path = os.path.join(input_folder, file_name)
        # Build name and path for output TIF file
        tif_name = os.path.splitext(file_name)[0] + ".tif"
        tif_path = os.path.join(output_folder, tif_name)

        # Open the JP2 file and convert it to a TIF file
        with rasterio.open(jp2_path) as src:
            rio_shutil.copy(src, tif_path, driver="GTiff")

        print(f"Converted: {file_name} -> {tif_name}")

print("Processing complete!")