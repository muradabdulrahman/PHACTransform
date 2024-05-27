'''
Usage:

python concatenate_CSVs.py <source_dir> <target_dir>

----------------

This script concatenates all the CSV files in the source directory into a single CSV file in the target directory.
    
'''

import sys

def concatenate_csvs(directory):
    # Get list of CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # Initialize an empty DataFrame
    df = pd.DataFrame()

    # Process each file
    for csv_file in csv_files:
        # Load the CSV data into a DataFrame
        data = pd.read_csv(os.path.join(directory, csv_file))

        # Append the data to the main DataFrame
        df = pd.concat([df, data])

    # Print the number of rows in the DataFrame
    print(f'Total number of rows: {len(df)}')

if __name__ == "__main__":
    output_directory = sys.argv[1]
    concatenate_csvs(output_directory)
