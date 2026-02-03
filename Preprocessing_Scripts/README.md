# Preparing Images for use with UrbanWatch

## Convert files to the correct image format
### Do one of the following:
- If the images were downloaded in the compressed **JP2** format, run *convert_JP2_to_TIF.py* to convert them to TIF file format before preprocessing.
- If the images were downloaded in **TIF** format in compressed zip folders, use *extractZIP.py* to extract the full-size images. This step is *required* if the images were downloaded in compressed zip folders before you can preprocess them.

## Preprocess images for UrbanWatch LULC classification
- With the images in TIF format, run *preprocessNAIP.py* to reorder the bands to create a false color composite and then resample the images to 1-m resolution.

## Optional Step
- If the images were downloaded in full-size TIF format, the images can be compressed to JP2 format using *convert_TIF_to_JP2.py* to reduce size before saving them to a cloud location.
