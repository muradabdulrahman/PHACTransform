'''
This program moves files from one directory to another based on a reference CSV file. 
The CSV file has the filenames to move (only Human DMS files) in the second column.
The program reads the CSV file, loops over the filenames in the second column, and moves the files from the source directory to the target directory.
'''

import shutil
import pandas as pnd
import os

# Define the paths
source_dir = "./DMS_ProteinGym_substitutions" # The directory where the DMS files are currently stored
target_dir = './DMS_Human' # The directory where the human DMS files should be moved to
reference_csv = './DMS_Human.csv' # The CSV file that contains the filenames to move (the filtered metadata)

# Read the reference CSV
df = pnd.read_csv(reference_csv)

# Loop over the filenames in the second column
for filename in df.iloc[:, 1]:
    print(filename)
    source_path = os.path.join(source_dir, filename)
    target_path = os.path.join(target_dir, filename)

    # Check if the file exists in the source directory
    if os.path.exists(source_path):
        # Move the file
        shutil.move(source_path, target_path)
