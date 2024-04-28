## Workflow of the Scripts

#### 1. create_config.py

```
python create_config.py -mut <mutation_file_path> -qry <query_fasta_file_path>
```
##### input arguments:
- -mut, --mutfilepath: Path to the mutation-scores file (CSV format).
- -qry, --queryfilepath: Path to the query FASTA file consists of all the protein sequences in the DMS database.

##### outputs:

* create directories if not exist for other scripts to save embedding files
  > folder_path1 = "./embeddings"
  >
  > folder_path2 = "./embeddings/mutation_seq"
  >
  > folder_path3 = "./embeddings/mutations_embeddings"
  >
  > folder_path4 = "./embeddings/input_tensors"
  
* creates config file for array-wise submission and saves it to `./embeddings`
  > Example:
  > 
  >ArrayID	sequence_name
  >
  > 1	XXXX_1
  >
  > 2	XXXX_2
  >
  > 3	XXXX_3

* creates embeddings for all the WT-sequences, it uses `./esm_extract.py` script `esm2_t33_650M_UR50D` model for bulk submission. It saves them to `./embeddings/WT_embeddings` directory with .pt extention

___________________________________

#### 2. create_embeddings.py

```
python create_embeddings.py -mut <mutation_file_path> -qry <query_fasta_file_path> -seq <protein_sequence_name>
```
##### input arguments:
- -mut, --mutfilepath: Path to the mutation-scores file (CSV format).
- -qry, --queryfilepath: Path to the query FASTA file consists of all the protein sequences in the DMS database.
- -seq, --protein_seq: Name of the protein sequence (ID) to mutate.

##### outputs:

* With the given protein ID, it retrieves the sequence from query fasta file and change the aminoacid given position to given amino acid as it is written in the mutation-scores file. The mutated sequences saved to `./embeddings/mutation_seq/{PROTEIN_ID}_mutations.fasta`
* creates embeddings for all the mutations given protein ID and saves these embeddings to `./embeddings/mutations_embeddings/{sequence_name}_mutations_embedding` folder as .pt extension.

  
  ![image](https://github.com/muradabdulrahman/PHACTransform/assets/100361704/67f7141a-7b0d-469f-93bd-cc10850e9378)


___________________________________


#### 3. create_input_matrix.py

```
python create_input_matrix.py -mut <mutation_file_path> -seq <protein_sequence_name>
```
##### input arguments:
- -mut, --mutfilepath: Path to the mutation-scores file (CSV format).
- -seq, --protein_seq: Name of the protein sequence (ID) to mutate.

##### outputs:

* it loops in the mutation embeddings folder of given protein ID. It stores WT embedding, mutation embedding, PHACT score, and DMS score in a matrix and then saves it as `./embeddings/input_tensors/{protein_ID+mutation}.pt`

```
        matrix_list = [sequence_representation_wt, sequence_representation, torch.tensor(phact_score),
                       torch.tensor(dms)]
        torch.save(matrix_list, f'./embeddings/input_tensors/{name}.pt')

```


![image](https://github.com/muradabdulrahman/PHACTransform/assets/100361704/507955f4-856f-4555-91a6-6db1eda2ebf9)

