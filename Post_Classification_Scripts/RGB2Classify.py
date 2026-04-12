"""
Script Name: RGB to Classified Raster Conversion

### Execution Environment:
- This script must be run in an ArcGIS Pro Python environment
- Ensure ArcGIS Pro is installed* and use its Python environment

### Purpose:
- Converts multi-band RGB images into single-band classified rasters.
- Uses a color lookup table (LUT) to map RGB values to predefined class IDs.

### Input:
- A folder containing RGB raster images (3-band TIFFs ).

### Output:
- Output is saved in a designated folder
"""

import os
import arcpy
import numpy as np
from arcpy.sa import *

# Enable Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

# Define input and output folders
input_folder = r"REPLACE-WITH-PATH-TO-INPUT-FOLDER"
output_folder = r"REPLACE-WITH-PATH-TO-OUTPUT-FOLDER"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Color lookup table (RGB -> Class ID)
color_to_class = {
    (255, 0, 0): 0,
    (133, 133, 133): 1,
    (255, 0, 192): 2,
    (34, 139, 34): 3,
    (128, 236, 104): 4,
    (255, 193, 37): 5,
    (0, 0, 255): 6,
    (128, 0, 0): 7,
    (255, 255, 255): 8
}

# Set workspace to input folder and get the list of raster files
arcpy.env.workspace = input_folder
raster_list = arcpy.ListRasters()

# Loop through each raster file in the input folder
for raster in raster_list:
    print(f"Processing: {raster}")

    # Read the RGB raster
    raster_path = os.path.join(input_folder, raster)
    bands = [Raster(raster_path + f"\\Band_{i}") for i in range(1, 4)]

    # Get spatial information from the raster
    desc = arcpy.Describe(raster_path)
    lower_left = desc.extent.lowerLeft  # Get lower-left corner of the raster
    spatial_ref = desc.spatialReference  # Get spatial reference (projection)

    # Get cell size (pixel resolution)
    cell_size_x = float(arcpy.GetRasterProperties_management(raster_path, "CELLSIZEX").getOutput(0))
    cell_size_y = float(arcpy.GetRasterProperties_management(raster_path, "CELLSIZEY").getOutput(0))

    # Convert raster bands to NumPy arrays
    red_band = arcpy.RasterToNumPyArray(bands[0])
    green_band = arcpy.RasterToNumPyArray(bands[1])
    blue_band = arcpy.RasterToNumPyArray(bands[2])

    # Get raster dimensions
    rows, cols = red_band.shape

    # Stack RGB channels into a single array
    rgb_pixels = np.dstack((red_band, green_band, blue_band))

    # Initialize an empty classification array with a default NoData value (-1)
    class_array = np.full((rows, cols), -1, dtype=np.int16)  # Using int16 to prevent overflow issues

    # Loop through the color lookup table and assign class IDs
    for color, class_id in color_to_class.items():
        mask = (rgb_pixels[:, :, 0] == color[0]) & \
               (rgb_pixels[:, :, 1] == color[1]) & \
               (rgb_pixels[:, :, 2] == color[2])
        class_array[mask] = class_id  # Assign class ID to matching pixels

    # Convert NumPy array back to an ArcGIS Raster
    class_raster = arcpy.NumPyArrayToRaster(class_array, lower_left, cell_size_x, cell_size_y, value_to_nodata=-1)

    # Set the projection to match the input raster
    arcpy.DefineProjection_management(class_raster, spatial_ref)

    # Save the classified raster to the output folder
    output_raster = os.path.join(output_folder, os.path.splitext(raster)[0] + "_classified.tif")
    class_raster.save(output_raster)

    print(f"Saved classified raster: {output_raster}")

print("Processing completed.")
