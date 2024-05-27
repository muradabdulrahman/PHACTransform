# Data Pre-processing

The PHACTransform project utilizes two different datasets: DMS score data from [ProteinGym](https://proteingym.org/) and PHACT scores from [PHACTboost](https://www.biorxiv.org/content/10.1101/2024.01.30.577938v1).

## DMS Data

The DMS dataset includes deep mutational scanning scores from 217 proteins of various species. In this project, we focused solely on human proteins. To extract and shape the data accordingly, we implemented the following steps. Initially, we filtered the dataset to include only human proteins and excluded unreliable and redundant data, resulting in a selection of 81 out of 96 human proteins for preprocessing.

### Data Preparation

#### Gathering Human DMS Data

To retrieve only the human proteins from the entire dataset, we utilized the [`gatherHumanDMS.py`](./scripts/gatherHumanDMS.py) script with the [filtered metadata](filtered_DMS_human_metadata.csv).

#### Renaming Files

The initial data files were named according to the protein names, species, and experiments, including unnecessary parts. To maintain consistency, we decided to rename the files using UniProt IDs. First, we extracted the protein names from the file names with the [`abstract_protein_names.py`](./scripts/abstract_protein_names.py) script, which writes the protein names into a CSV file named `protein_names.csv`. UniProt IDs were then manually added to the CSV file and used for renaming the DMS score files with the [`rename_DMS_files.py`](./scripts/rename_DMS_files.py) script.

### Normalization of the DMS Scores

#### Normalization and Reshaping of the Data

DMS scores, generated from different experiments, varied in scaling. To provide consistent scores for the model, we normalized them. The initial data format included both SNPs and indel mutations. Since our project focuses on single amino acid mutations, we filtered out other mutation types. Additionally, we added UniProt IDs to each DMS file. This step was performed using the [`normalizeDMSscores.py`](./scripts/normalizeDMSscores.py) script.

#### Concatenating the DMS Score Files

After reshaping and normalizing the data, we concatenated all DMS score files into a single file using the [`concatenate_CSVs.py`](./scripts/concatenate_CSVs.py) script.

## Gathering FASTA Files of the Proteins

The FASTA files for the entire human proteome were already available in the PHACTboost dataset. We used the [`copy_fasta_files.py`](./scripts/copy_fasta_files.py) script to gather the FASTA files in one location to feed the model later.

## PHACTboost Data

#### Transforming the PHACT Score Data

The PHACT scores were initially formatted as a matrix of (protein length) x (twenty common amino acids), storing all possible single amino acid mutation scores for a protein. We needed these mutations and scores in columns. The [`transform_score_files.py`](./scripts/transform_score_files.py) script was used to gather and transform the PHACT scores from the PHACTboost dataset.

#### Concatenating the PHACT Score Files

After transforming and gathering the data, we concatenated all PHACT score files into one using the [`concatenate_CSVs.py`](./scripts/concatenate_CSVs.py) script.

## Merging Final Datasets

After completing all data preprocessing steps, the final concatenated CSV files of PHACT and DMS scores were merged into a single file using the [`merge_CSVs.py`](./scripts/merge_CSVs.py) script.


!!!!!!!!!!!!!!!!!

In the final merged file there are only substitions that are matching in both concatenated DMS and PHACT score CSVs. I noticed that some of the substitutions are missed in the final CSV. The reason for that is the DMS score files nnot uses the exact amino acid positions in their substitution annotaions.

This is an example of the final normalized CSV of a protein:
```
query_id,mutant,mutated_sequence,DMS_score,DMS_score_bin
O00257,A1C,CVESIEKKRIRKGRVEYLVKWRGWSPKYNTWEPEENILDPRLLIAFQNRE,0.9402990147122778,1
O00257,A1D,DVESIEKKRIRKGRVEYLVKWRGWSPKYNTWEPEENILDPRLLIAFQNRE,0.8690069752655201,1
O00257,A1E,EVESIEKKRIRKGRVEYLVKWRGWSPKYNTWEPEENILDPRLLIAFQNRE,0.9247180481451349,1
```
If you look at the "mutant"s the position "1" is corresponding to the position of amino acid "A" in the "mutated_sequence". Normally position 1st should me "M". Because of this some of the mutaitons are not matching with the PHACTdata when merging CSVs and it resuşts with some losts. This mutated sequence is different for each protein in the data set and refers to the part of the protein that are used in DMS experiments. But partial sequence usage is not the case for all of the proteins. I think only some of them has partial ones. It is stated in the mutated [metadata table](filtered_DMS_human_metadata.csv) under the "region_mutated" section.

Ading an extra checking step to the preprocessing step can solve this. These annotations should be re-written with correct positions of the amino acisds in order to match with the PHACT data. To do that, a script that will search the mutated region in the actual sequence of the protein and find the true corresponding position in the whole sequence can solve the problem. After finding the correct position annonations of the substitions could be re-written. 
