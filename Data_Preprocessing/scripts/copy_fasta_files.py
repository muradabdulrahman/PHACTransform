'''
Usage:

python copy_fasta_files.py <source_dir> <target_dir> <csv_file>

----------------

This script copies the fasta files for the protein IDs listed in the CSV file from the source directory to the target directory.

'''

import csv
import os
import shutil
import sys

def copy_fasta_files(source_dir, target_dir, csv_file):
    # Read the CSV file and get the protein IDs
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        protein_ids = [row[0] for row in reader]

    # Initialize counters
    total_proteins = len(protein_ids)
    copied_files_count = 0
    not_found_count = 0

    # For each protein ID, copy the fasta file to the target directory
    for protein_id in protein_ids:
        fasta_file = os.path.join(source_dir, protein_id, "1_psiblast", protein_id + ".fasta")
        if os.path.exists(fasta_file):
            shutil.copy(fasta_file, target_dir)
            copied_files_count += 1
        else:
            print(f"Error: Fasta file for protein {protein_id} not found in source directory.")
            not_found_count += 1

    # Print the final counts
    print(f"Total protein IDs: {total_proteins}")
    print(f"Number of fasta files copied: {copied_files_count}")
    print(f"Number of fasta files not found: {not_found_count}")

if __name__ == "__main__":
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    csv_file = sys.argv[3]
    copy_fasta_files(source_dir, target_dir, csv_file)
