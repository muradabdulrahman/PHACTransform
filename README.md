# PHACTransform
CS-515 Deep Learning class project

## Abstract

Mutations are pivotal in biology, driving genetic diversity and influencing various biological processes. Predicting the effects of mutations accurately remains challenging due to genetic complexity and vast genomic data. Deep Mutational Scanning (DMS) offers insights into protein function and genetic diversity but is resource-intensive. Computational tools like EVE (Evolutionary Model of Variant Effect) and Rep2Mut-V2 leverage sequence alignments and deep learning to predict mutation effects efficiently. However, these methods often lack precision in capturing biological complexities.
We introduce **PHACTransform**, a novel approach integrating multiple sequence alignments (MSA), evolutionary data, and experimental DMS scores into deep learning models for precise variant effect prediction. By incorporating PHACT-based measures and DMS scores, our approach aims to enhance mutation effect predictions beyond conventional methods. Our research contributes to advancing genetic variation understanding, impacting drug discovery, personalized medicine, and evolutionary biology.


## Data Pre-processing 
<details>

The PHACTransform project utilizes two different datasets: DMS score data from [ProteinGym](https://proteingym.org/download) and PHACT scores from [PHACTboost](https://www.biorxiv.org/content/10.1101/2024.01.30.577938v1).


The DMS dataset includes deep mutational scanning scores from 217 proteins of various species. In this project, we focused solely on human proteins. To extract and shape the data accordingly, we implemented the following steps. Initially, we filtered the dataset to include only human proteins and excluded unreliable and redundant data, resulting in a selection of 81 out of 96 human proteins for preprocessing.

### Data Preparation 

#### Gathering Human DMS Data

To retrieve only the human proteins from the entire dataset, we utilized the [`gatherHumanDMS.py`](./scripts/gatherHumanDMS.py) script with the [filtered metadata](filtered_DMS_human_metadata.csv).

#### Renaming Files

The initial data files were named according to the protein names, species, and experiments, including unnecessary parts. To maintain consistency, we decided to rename the files using UniProt IDs. First, we extracted the protein names from the file names with the [`abstract_protein_names.py`](./scripts/abstract_protein_names.py) script, which writes the protein names into a CSV file named `protein_names.csv`. UniProt IDs were then manually added to the CSV file and used for renaming the DMS score files with the [`rename_DMS_files.py`](./scripts/rename_DMS_files.py) script.

#### Correcting the Annotations of the Mutations
In some DMS experiments, partial protein sequences were used instead of whole sequences. The mutation positions were annotated based on these partial sequences. To prevent mapping errors with the PHACT score data (which uses the original positions from whole sequences), we updated the annotations using the [`change_annotations.py`](./scripts/change_annotations.py) script. During this process, we discovered that for some proteins, the mutated sequences did not match the sub-sequences of the original (canonical) protein sequences. Consequently, we eliminated those 18 proteins, resulting in a dataset of 230,209 data points (mutations) from 68 proteins.

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

</details>
