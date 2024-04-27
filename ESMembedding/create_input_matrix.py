"""
python create_input_matrix.py -mut <mutation_file_path> -seq <protein_sequence_name>

Arguments:
----------
- -mut, --mutfilepath: Path to the mutation file (CSV format).
- -seq, --protein_seq: Name of the protein sequence to process.

This script performs the following steps:

1. Parses command-line arguments to specify the path to the mutation file and the name of the protein sequence to process.
2. Defines directory paths for storing mutated embeddings and WT embeddings.
3. Loads the WT embedding for the specified protein sequence.
4. Reads the mutation file (CSV format) into a pandas DataFrame.
5. Filters mutations from the DataFrame based on the provided protein sequence name.
6. Iterates over mutated embedding files in the mutations embeddings directory.
7. Loads each mutated embedding file and extracts the mutation name, Phact score, DMS score, and sequence representation.
8. Creates input tensors consisting of WT and mutated sequence representations, Phact score, and DMS score.
9. Saves the input tensors as PyTorch tensors in the input tensors directory.

Note:
-----
Ensure that the WT embeddings and mutated embeddings are available in the specified directories for successful execution.
"""
import os
import pandas as pd
import torch
import argparse

parser = argparse.ArgumentParser(description='parse LASTZ output')
parser.add_argument('-mut', '--mutfilepath')
parser.add_argument('-seq', '--protein_seq')
args = parser.parse_args()

#################
sequence_name = args.protein_seq
mut_DIRECTORY = f"./embeddings/mutations_embeddings/{sequence_name}_mutations_embedding"
wt_embedding = f"./embeddings/WT_embeddings/{sequence_name}.pt"
#################

model_wt = torch.load(wt_embedding)
sequence_representation_wt = model_wt['mean_representations'][33]
MUTATION_FILE = args.mutfilepath
mut_df = pd.read_csv(MUTATION_FILE)
df = mut_df[mut_df['QueryID'] == sequence_name]

for filename in os.listdir(mut_DIRECTORY):
    embed_file = os.path.join(mut_DIRECTORY, filename)
    if os.path.isfile(embed_file):
        model = torch.load(embed_file)
        name = model['label']
        mut = name.split('_')[-1]
        phact_score = df[df['Substitution'] == mut]['PHACT_score'].values[0]
        dms = df[df['Substitution'] == mut]['DMS_score'].values[0]
        sequence_representation = model['mean_representations'][33]
        # print(filename)
        # print('protein name: ' + name)
        # print('mutation: ' + mut)
        # print(f'Phact Score: {phact_score}')
        # print(f'DMS Score: {dms}')
        # print(f'Seq representation:\n{sequence_representation}')
        # print(type(sequence_representation))

        matrix_list = [sequence_representation_wt, sequence_representation, torch.tensor(phact_score),
                       torch.tensor(dms)]
        torch.save(matrix_list, f'./embeddings/input_tensors/{name}.pt')
