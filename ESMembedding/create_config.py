"""
Usage:
------
python create_config.py -mut <mutation_file_path> -qry <query_fasta_file_path>

Arguments:
----------
- -mut, --mutfilepath: Path to the mutation file (CSV format).
- -qry, --queryfilepath: Path to the query FASTA file.

This script performs the following steps:

1. Parses command-line arguments to specify the paths to the mutation file and query FASTA file.
2. Creates necessary folders for storing intermediate and output files.
3. Writes a configuration file ('config.txt') to map ArrayIDs to sequence names.
4. Extracts wild-type (WT) embeddings from the query FASTA file using the ESM model.
   The embeddings are stored in the 'WT_embeddings' folder.

Note:
-----
Ensure that the ESM model (esm2_t33_650M_UR50D) and the 'esm_extract.py' script are available in the current working
directory or specified in the system PATH for successful execution.

"""
from Bio import SeqIO
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='parse LASTZ output')
parser.add_argument('-mut', '--mutfilepath')
parser.add_argument('-qry', '--queryfilepath')
args = parser.parse_args()

MUTATION_FILE = args.mutfilepath
QUERY_FASTA_FILE = args.queryfilepath


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


folder_path1 = "./embeddings"
folder_path2 = "./embeddings/mutation_seq"
folder_path3 = "./embeddings/mutations_embeddings"
folder_path4 = "./embeddings/input_tensors"
create_folder_if_not_exists(folder_path1)
create_folder_if_not_exists(folder_path2)
create_folder_if_not_exists(folder_path3)
create_folder_if_not_exists(folder_path4)

fasta_file = QUERY_FASTA_FILE
idx = 0

# Config file for array-wise submission
with open('./embeddings/config.txt', mode='w') as f:
    f.write(f'ArrayID\tsequence_name\n')
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence_name = record.id
        idx += 1
        f.write(f'{idx}\t{sequence_name}\n')

# WT embeddings
WT_command = (f"python ./esm_extract.py esm2_t33_650M_UR50D {QUERY_FASTA_FILE} ./embeddings/WT_embeddings "
              f"--repr_layers 0 32 33 --include mean per_tok")

subprocess.run(WT_command, check=True)
