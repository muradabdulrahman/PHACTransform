'''
The program reads the filenames in the directory, extracts the protein names from the filenames, and writes them to a csv file.
After obtaining the protein names, the Uniprot IDs of proteins are manually added to the csv file. 
''' 

import os

def write_filenames_to_txt(directory, output_file):
    with open(output_file, 'w') as f:
        for filename in os.listdir(directory):
            f.write(filename.split("_")[0] +"_"+ filename.split("_")[1] + "," +'\n')

directory = './DMS_Human'

output_file = './protein_names.csv'

write_filenames_to_txt(directory, output_file)
