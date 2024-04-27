"""
Usage:
------
python create_embeddings.py -mut <mutation_file_path> -qry <query_fasta_file_path> -seq <protein_sequence_name>

Arguments:
----------
- -mut, --mutfilepath: Path to the mutation file (CSV format).
- -qry, --queryfilepath: Path to the query FASTA file.
- -seq, --protein_seq: Name of the protein sequence to mutate.

This script performs the following steps:

1. Parses command-line arguments to specify the paths to the mutation file, query FASTA file, and the name of
the protein sequence to mutate.
2. Reads the mutation file (CSV format) into a pandas DataFrame.
3. Retrieves the protein sequence from the query FASTA file based on the provided protein sequence name.
4. Filters mutations from the mutation DataFrame based on the provided protein sequence name.
5. Generates mutated sequences based on the retrieved protein sequence and mutations, and writes them to a FASTA file.
6. Extracts embeddings for the mutated sequences using the ESM model.
7. Saves the embeddings to the 'mutations_embeddings' folder.

Note:
-----
Ensure that the ESM model (esm2_t33_650M_UR50D) and the 'esm_extract.py' script are available in the current working
directory or specified in the system PATH for successful execution.

"""

import subprocess
import pandas as pd
from Bio import SeqIO
import argparse


def get_sequence_from_fasta(fasta_file, protein_name):
    """
    Function to retrieve the sequence from a FASTA file given the protein name.

    Parameters:
    - fasta_file (str): Path to the FASTA file.
    - protein_name (str): Name of the protein to search for.

    Returns:
    - str: Sequence corresponding to the protein name, or None if not found.
    """
    sequence = None
    # Create an index of sequences in the FASTA file
    index = SeqIO.index(fasta_file, "fasta")
    # Retrieve the sequence corresponding to the protein name
    if protein_name in index:
        sequence = str(index[protein_name].seq)
    return sequence


parser = argparse.ArgumentParser(description='parse LASTZ output')
parser.add_argument('-mut', '--mutfilepath')
parser.add_argument('-qry', '--queryfilepath')
parser.add_argument('-seq', '--protein_seq')
args = parser.parse_args()


MUTATION_FILE = args.mutfilepath
mut_df = pd.read_csv(MUTATION_FILE)
fasta_file = args.queryfilepath
#################
sequence_name = args.protein_seq
MUTATED_SEQUENCES = f'./embeddings/mutation_seq/{sequence_name}_mutations.fasta'
#################

protein_sequence = get_sequence_from_fasta(fasta_file, sequence_name)
df = mut_df[mut_df['QueryID'] == sequence_name]
mutations = df['Substitution'].tolist()

with open(MUTATED_SEQUENCES, mode='w') as f:
    for index, mutation in enumerate(mutations):
        org = mutation[0]
        pos = int(mutation[1])
        var = mutation[2]

        if protein_sequence[pos-1] != org.upper():
            raise KeyError

        mutated_sequence = protein_sequence[:pos-1] + var.upper() + protein_sequence[pos:]
        f.write(f'>{sequence_name}_{org.upper()}{pos}{var}\n')
        f.write(f'{mutated_sequence}\n')


Mutations_command = f"python ./esm_extract.py esm2_t33_650M_UR50D {MUTATED_SEQUENCES} ./embeddings/mutations_embeddings/{sequence_name}_mutations_embedding --repr_layers 0 32 33 --include mean per_tok"

subprocess.run(Mutations_command, check=True)

