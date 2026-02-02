# extractZIP.py
# Extracts contents of all zipped folders in the source directory
# For imagery, used when full resolution images are downloaded as zipped folders
# User must set the source and destination folder paths

import os
import zipfile

def extract_zipped_files(src_folder, dest_folder):
    # Iterate through all items in the source folder
    for i in os.listdir(src_folder):
        # Check if the current item is a zipped folder
        if i.lower().endswith('.zip'):
            file_path = os.path.join(src_folder, i)
            
            try:
                # Open the zipped folder and extract its contents
                with zipfile.ZipFile(file_path, 'r') as zipped:
                    # Iterate through all files in the zipped folder
                    for file in zipped.namelist():
                        # Extract each file to the destination folder
                        zipped.extract(file, dest_folder)
                        print(f"Extracted {file} to {dest_folder}")
                    print("Extraction complete!")
            except zipfile.BadZipFile:
                print(f"Failed to extract {i}. Not a valid zip file.")
            except Exception as e:
                print(f"Error extracting {i}: {e}")

# Set source and destination folders
src_folder = r"REPLACE-WITH-PATH-TO-SOURCE-FOLDER"  
dest_folder = r"REPLACE-WITH-PATH-TO-DESTINATION-FOLDER"

# If destination folder doesn't exist, create it
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

# Call the function to extract all zip files
extract_zipped_files(src_folder, dest_folder)