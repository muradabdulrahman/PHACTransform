'''
This program renames the human DMS files in a directory based on the reference protein_names.csv file.
It reads the reference CSV file, loops over the rows, finds the file that starts with the prefix, and renames it to the new name.
The new name is constructed using the protein ID, prefix, and the original filename.
'''


import pandas as pd
import os
import shutil

# Define the paths
source_dir = './files_with_old_names' # The directory where the DMS files are currently stored
target_dir = './Names_updated' # The directory where the renamed files should be written to
reference_csv = './protein_names.csv' # The CSV file that contains the protein names and UniProt IDs

# Read the reference CSV
df = pd.read_csv(reference_csv, header=None)

# Loop over the rows in the DataFrame
for index, row in df.iterrows():
    prefix, protein_id = row[0], row[1]

    # Find the file that starts with the prefix
    for filename in os.listdir(source_dir):
        if filename.startswith(prefix):
            # Construct the new filename and the source and target paths
            new_filename = f'{protein_id}_{prefix}_DMS_scores.csv'
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, new_filename)

            # Copy the file to the target directory with the new name
            shutil.copy(source_path, target_path)
