# preprocessNAIP.py
# Reorders NAIP image bands to red false color composite
#   >   Valid for imagery from 2009 or later (with NIR band)
# Resamples the image to 1-meter resolution
# User must set the source and destination directories

import os
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.transform import from_bounds
from rasterio.warp import reproject

# Set the source and destination directories
src_folder = r"REPLACE-WITH-PATH-TO-SOURCE-FOLDER"  
dest_folder = r"REPLACE-WITH-PATH-TO-DESTINATION-FOLDER"

# Ensure the destination folder exists
os.makedirs(dest_folder, exist_ok=True)

# Set the band order for false color composite ([NIR, Red, Green])
fcc_bands = [4, 3, 2]  

# Set the new resolution in meters
new_resolution = 1

# Iterate through all files in the source folder
for file in os.listdir(src_folder):
    # Check for TIF or TIFF files
    if file.lower().endswith((".tif", ".tiff")):
        # Build name and path for output images
        src_path = os.path.join(src_folder, file)
        dest_path = os.path.join(dest_folder, file)

        with rasterio.open(src_path) as src:
            # Get source metadata and transform
            src_transform = src.transform
            src_crs = src.crs
            src_bounds = src.bounds
            src_dtype = src.dtypes[0]  

            # Calculate new transform and dimensions
            new_width = int((src_bounds.right - src_bounds.left) / new_resolution)
            new_height = int((src_bounds.top - src_bounds.bottom) / new_resolution)
            new_transform = from_bounds(
                src_bounds.left, src_bounds.bottom,
                src_bounds.right, src_bounds.top,
                new_width, new_height
            )

            # Read and reorder bands for false color composite
            bands = []
            for band_idx in fcc_bands:
                band_data = src.read(band_idx)
                bands.append(band_data)

            # Resample bands to target resolution
            resampled_bands = []
            for band_data in bands:
                destination = np.empty((new_height, new_width), dtype=src_dtype)
                reproject(
                    source=band_data,
                    destination=destination,
                    src_transform=src_transform,
                    src_crs=src_crs,
                    dst_transform=new_transform,
                    dst_crs=src_crs,
                    resampling=Resampling.bilinear
                )
                resampled_bands.append(destination)

            # Write preprocessed image to output
            with rasterio.open(
                dest_path,
                'w',
                driver='GTiff',
                height=new_height,
                width=new_width,
                count=len(resampled_bands),
                dtype=src_dtype,
                crs=src_crs,
                transform=new_transform
            ) as dst:
                for i, resampled_band in enumerate(resampled_bands, start=1):
                    dst.write(resampled_band, i)

        print(f"Processed and saved: {file}")

print("Processing complete!")