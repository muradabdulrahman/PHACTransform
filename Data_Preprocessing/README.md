# Data Pre-processing

The PHACTransform project uses two different dataset: DMS score dataset from [ProteinGym](https://proteingym.org/) and PHACT scores from [PHACTboost](https://www.biorxiv.org/content/10.1101/2024.01.30.577938v1).

## DMS Data

DMS data includes deep mutatinoal scanning scores from 217 proteins of various different species. In this project, we only focued on human proteins. In order to gather only human proteins and shape the data as we need, following steps are utilized.
Before begining the preprocessing, the dataset is filetred. First we filtered the metadata as it will only include the human proteins and then we filtered the unreliable and redundant data. And continued preprocessing with 81/96 human proteins.

### Gathering Human DMS data

For retrieving only the human proteins ot ouf the whole dataset, the gatherHumanDMS.py() script is utilized with filtered_DMS_metadata.csv()


The initial data filing was according to the names of the proteins, species, and exmperiments. Filenames included non-necesseray parts. In order to sustain the consistincy we decided to change the filenames using UniProt IDs of the proteins.



The initial data format included both SNPs 
