import pandas as pd
import glob
import os

def read_csv_files(pattern):
    # Use glob to find files matching the pattern
    files = glob.glob('*{}*.csv'.format(pattern))
    
    # Create an empty list to store DataFrames
    dfs = []
    
    # Iterate over each file
    for file in files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file, index_col = [0])
        # Extract the name of the CSV file without the extension
        file_name = os.path.splitext(os.path.basename(file))[0]
        city_name = file_name.split('_')[0]
        # Create a new column with the file name
        df['City'] = city_name
        # Append the DataFrame to the list
        dfs.append(df)

    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    
    return combined_df
