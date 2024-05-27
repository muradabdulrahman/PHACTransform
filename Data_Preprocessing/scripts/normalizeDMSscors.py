'''
This program reads the DMS scores from the CSV files, normalizes the scores, and saves the normalized scores to new CSV files.
The normalization process involves shifting the scores so that all values are positive, applying a log transformation, and then scaling the scores to the range [0, 1].
The program reads the reference CSV file that contains the DMS IDs and protein IDs, and then iterates over each row in the reference DataFrame.
For each row, it finds the corresponding CSV file, loads the dataset, filters out the single amino acid mutations, and applies the normalization process.
The normalized dataset is then saved to a new CSV file in the target directory.
'''

import pandas as pd
import numpy as np
import os
import glob
import re

# Define the directory where the CSV files are located
csv_directory = './Names_updated'
target_dir= './Normalized'
# Read the reference CSV file
reference_df = pd.read_csv('./DMS_Human.csv')

# Iterate over each row in the reference DataFrame
for index, row in reference_df.iterrows():
    # Retrieve the DMS ID
    dms_id = row['DMS_id'].split('_')[0]+"_"+row['DMS_id'].split('_')[1]

    # Find the CSV file that contains the DMS ID in its name
    csv_files = glob.glob(os.path.join(csv_directory, f'*{dms_id}*.csv'))
    if not csv_files:
        print(f"No CSV file found for DMS ID {dms_id}")
        continue
    csv_file = csv_files[0]

    # Extract the protein ID from the filename
    protein_id = os.path.basename(csv_file).split('_')[0]

    # Load the corresponding protein dataset
    protein_df = pd.read_csv(csv_file)

    # Define the regular expression pattern for single amino acid mutations
    pattern = r'^[A-Z][0-9]+[A-Z]$'

    # Apply the filter
    protein_df = protein_df[protein_df['mutant'].str.match(pattern)]

    # Add the protein ID as a new column at the beginning
    protein_df.insert(0, 'query_id', protein_id)

    # Shift the DMS scores so that all values are positive
    min_score = protein_df['DMS_score'].min()
    protein_df['DMS_score'] = protein_df['DMS_score'] + abs(min_score) + 1

    # Apply the log transformation to the DMS scores
    protein_df['DMS_score'] = np.log(protein_df['DMS_score'])

    # Normalize the DMS scores
    min_score = protein_df['DMS_score'].min()
    max_score = protein_df['DMS_score'].max()
    protein_df['DMS_score'] = (protein_df['DMS_score'] - min_score) / (max_score - min_score)

    # Construct the output filename
    output_filename = os.path.join(target_dir, f'{protein_id}_{dms_id}_DMS_scores_normalized.csv')

    # Split the filename into parts
    parts = output_filename.split('_')

    # Construct the new filename
    new_filename = parts[0] + '_' + '_'.join(parts[-3:])

    # Save the transformed and normalized dataset to a new CSV file with the new filename
    protein_df.to_csv(new_filename, index=False)
