'''
This program read DMS cores and PHACT scores from two CSV files, merges the data based on the 'query_id' and 'substitution' columns, and saves the merged data to a new CSV file.
'''

import pandas as pd

# Define the paths to the two CSV files
phact_scores = './phact_scores_concatenated.csv'
dms_scores ='./DMS_scores_concatenated.csv'

# Load the two CSV files
df1 = pd.read_csv(phact_scores)
df2 = pd.read_csv(dms_scores)

# Merge the dataframes based on 'query_id' and 'substitution'
merged_df = pd.merge(df2, df1, how='inner', on=['query_id', 'substitution'])

# Save the merged dataframe to a new CSV file
merged_df.to_csv('merged_scores.csv', index=False)
