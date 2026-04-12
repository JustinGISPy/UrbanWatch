# ImgClip.py
# Purpose: Batch clip raster GeoTIFF images using a vector shapefile (city boundary) while keeping the original image dimension
# Saves processed .tif files to user-specified folder.

import os
import glob
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def fix_geometries(gdf):
    """Fix invalid geometries safely."""
    invalid = ~gdf.is_valid
    if invalid.any():
        print(f"⚠ Fixing {invalid.sum()} invalid geometries")
        gdf.loc[invalid, "geometry"] = gdf.loc[invalid, "geometry"].buffer(0)
    return gdf

def align_vector_to_raster(gdf, raster_crs):
    """
    Align vector CRS to raster CRS in a safe, cross-platform way.
    """

    if gdf.crs is None:
        print("⚠ Vector CRS missing — assuming EPSG:4326")
        gdf = gdf.set_crs("EPSG:4326")

    xmin, ymin, xmax, ymax = gdf.total_bounds
    looks_geographic = (-180 <= xmin <= 180 and -180 <= xmax <= 180 and
                        -90 <= ymin <= 90 and -90 <= ymax <= 90)

    if looks_geographic and not gdf.crs.is_geographic:
        print("⚠ Vector CRS appears mislabeled — forcing EPSG:4326")
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)

    return gdf.to_crs(raster_crs)

# ------------------------------------------------------------
# Main processing function
# ------------------------------------------------------------

def batch_mask_rasters(raster_dir, shapefile_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Read and pre-clean vector once
    shapes_gdf = gpd.read_file(shapefile_path)
    shapes_gdf = fix_geometries(shapes_gdf)

    raster_files = glob.glob(os.path.join(raster_dir, "*.tif"))

    for raster_path in raster_files:
        filename = os.path.basename(raster_path)
        output_path = os.path.join(output_dir, filename)

        print(f"\nProcessing: {filename}")

        with rasterio.open(raster_path) as src:

            if src.crs is None:
                raise RuntimeError(f"❌ Raster CRS missing for {filename} — cannot process safely")

            # Align vector CRS to raster CRS
            shapes_proj = align_vector_to_raster(shapes_gdf, src.crs)

            # ----------------------
            # Linux/Windows-safe geometry filter
            # ----------------------
            geoms = [
                geom.__geo_interface__
                for geom in shapes_proj.geometry
                if geom is not None and not geom.is_empty and geom.is_valid and geom.area > 0
            ]

            if not geoms:
                # No valid geometry intersects — output zeros
                out_image = np.zeros(
                    (src.count, src.height, src.width),
                    dtype=src.dtypes[0]
                )
            else:
                # Safe mask for both platforms
                out_image, _ = mask(
                    src,
                    geoms,
                    crop=False,
                    nodata=0,
                    filled=True
                )

            # Replace raster nodata values with 0
            if src.nodata is not None:
                out_image[out_image == src.nodata] = 0

            out_image = np.nan_to_num(out_image, nan=0)

            # Update metadata and write output
            out_meta = src.meta.copy()
            out_meta.update({
                "nodata": None
            })

            with rasterio.open(output_path, "w", **out_meta) as dst:
                dst.write(out_image.astype(src.dtypes[0]))

            print("✅ Done")

    print("\n🎉 All rasters processed successfully")


# ------------------------------------------------------------
# Define your paths
# ------------------------------------------------------------

INPUT_DIR = r"REPLACE-WITH-PATH-TO-INTPUT-FOLDER"
SHAPEFILE = r"REPLACE-WITH-PATH-TO-BOUNDARY-SHAPEFILE" # With .shp file extension
OUTPUT_DIR = r"REPLACE-WITH-PATH-TO-OUTPUT-FOLDER"

batch_mask_rasters(INPUT_DIR, SHAPEFILE, OUTPUT_DIR)