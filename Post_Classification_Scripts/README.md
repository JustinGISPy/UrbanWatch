# Postprocessing images after running UrbanWatch

After performing LULC classification with UrbanWatch, the following scripts are used to finish processing the images.

## Add the projection to the images
- Use *projectTIF.py* to transfer the projection information from the input images to the UrbanWatch result images.

## Clip images to a boundary shapefile
- Use *ImgClip.py* to clip the projected UrbanWatch result images to the extent of a boundary shapefile.

## Convert to 1-band index images
- Use *RGB2Classify.py* to create 1-band index images. (Requires an **arcpy** Python environment)