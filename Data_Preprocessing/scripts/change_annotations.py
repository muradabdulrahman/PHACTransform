import pandas as pd
from Bio import SeqIO
import os
import shutil

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# The program above reads the protein names and the filtered DMS human metadata CSV files, merges them, and writes the mutated sequences to a new CSV file.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Read the CSV files
df1 = pd.read_csv('protein_names.csv')
df2 = pd.read_csv('filtered_DMS_human_metadata.csv')

# Merge the dataframes
merged = pd.merge(df1, df2, on='UniProt_ID')

# Select only the columns you want
result = merged[['UniProt_ID', 'ID', 'target_seq']]

# Write the result to a new CSV file
result.to_csv('mutated_sequences.csv', index=False)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# The program above reads the mutated sequences from the CSV file, compares them with the original sequences, and updates the annotations of the mutations accordingly.
# It loads the corresponding DMS files, updates the positions of the mutations, and writes the updated DMS files to a new directory.
# Change the paths as needed.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

DMS_score_path = './DMS_Human/Normalized'
fasta_path = './fasta_files'
output_dir = './updated_DMS_scores_normalized'

# Create a new directory for the updated DMS files
os.makedirs(output_dir, exist_ok=True)

# Load the mutated_sequences.csv into a pandas DataFrame
df = pd.read_csv('mutated_sequences.csv')

count_subseq = 0
count_not_equal = 0
IDs_to_remove = []

# For each row in the DataFrame
for index, row in df.iterrows():
    # Load the corresponding FASTA file
    fasta_file = fasta_path + row['ID'] + '.fasta'
    for record in SeqIO.parse(fasta_file, "fasta"):
        original_sequence = str(record.seq)

    # Compare the mutated sequence with the original sequence
    mutated_sequence = row['target_seq']
    if original_sequence != mutated_sequence:
        count_not_equal+=1
        if mutated_sequence in original_sequence:
            count_subseq+=1

            # Find the starting position of the mutated sequence in the original sequence
            start_position = original_sequence.index(mutated_sequence)

            # Load the corresponding DMS_scores_normalized.csv file into a pandas DataFrame
            dms_file = DMS_score_path + row['ID'] + '_DMS_scores_normalized.csv'
            dms_df = pd.read_csv(dms_file)

            # For each row in the DMS DataFrame
            for dms_index, dms_row in dms_df.iterrows():
                # Extract the position from the 'mutant' column
                position = int(dms_row['mutant'][1:-1])

                # Add the starting position of the mutated sequence to the position
                new_position = start_position + position

                # Update the 'mutant' column with the new position
                dms_df.at[dms_index, 'mutant'] = dms_row['mutant'][0] + str(new_position) + dms_row['mutant'][-1]

            # Write the DMS DataFrame to the new directory
            new_dms_file = output_dir + row['ID'] + '_DMS_scores_normalized.csv'
            dms_df.to_csv(new_dms_file, index=False)

        else:
            IDs_to_remove.append(row['ID'])

    else:
        # If the sequences are the same, copy the DMS file to the new directory
        dms_file = DMS_score_path + row['ID'] + '_DMS_scores_normalized.csv'
        new_dms_file = output_dir + row['ID'] + '_DMS_scores_normalized.csv'
        shutil.copyfile(dms_file, new_dms_file)

print(count_subseq, count_not_equal, IDs_to_remove, len(IDs_to_remove))
