'''
Usage:

python transform_score_files.py <source_dir> <target_dir> <fasta_dir>

----------------

This script transforms the scores from the CSV files into a format that can be used for the analysis. 
The transformed data is saved to a new CSV file with the same name as the original file, but with "_transformed" appended to the name.

'''

import csv
import os
import pandas as pd
import sys

def transform_score_files(source_dir, target_dir, fasta_dir, protein_id):
    # Define the CSV file with scores and the fasta file with the sequence
    csv_file = os.path.join(source_dir, protein_id, "8_iqtree_ancestral_scores", protein_id + "_wl_param_CountNodes_3.csv")
    fasta_file = os.path.join(fasta_dir, protein_id + ".fasta")

    # Read the CSV file and get the scores
    scores = pd.read_csv(csv_file)

    # Read the fasta file and get the sequence
    with open(fasta_file, 'r') as f:
        sequence = f.readlines()[1].strip()

    # Create a list to store the transformed data
    transformed_data = []

    # For each position and amino acid, create a new row in the DataFrame
    for i, row in scores.iterrows():
        for aa, score in row.iteritems():
            if aa != 'Pos/AA':
                transformed_data.append({
                    'positions': i + 1,
                    'substitution': sequence[i] + str(i + 1) + aa,
                    'phact_score': score
                })

    # Convert the list to a DataFrame
    transformed_data = pd.DataFrame(transformed_data)

    # Write the transformed data to a new CSV file
    transformed_data.to_csv(os.path.join(target_dir, protein_id + "_wl_param_CountNodes_3_transformed.csv"), index=False)

if __name__ == "__main__":
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    fasta_dir = sys.argv[3]

    # Get the protein IDs from the names of the fasta files
    protein_ids = [os.path.splitext(f)[0] for f in os.listdir(fasta_dir) if f.endswith('.fasta')]

    # Apply the transformation to each protein
    for protein_id in protein_ids:
        transform_score_files(source_dir, target_dir, fasta_dir, protein_id)
