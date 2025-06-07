import os
import pandas as pd
import glob

# Path to the datasets directory
datasets_path = 'datasets'

# Get all CSV files in the datasets directory
csv_files = glob.glob(os.path.join(datasets_path, '*.csv'))

# Check if any CSV files were found
if not csv_files:
    print("No CSV files found in the datasets directory.")
    exit(1)

# List to store individual dataframes
dfs = []

# Read each CSV file
for csv_file in csv_files:
    # Extract year information from filename
    filename = os.path.basename(csv_file)
    # Add filename as a column to identify the season
    df = pd.read_csv(csv_file)
    
    # Extract season information from filename (e.g., 2023_24 from nba_player_stats_2023_24_per_game.csv)
    season = filename.split('_')[3] + '_' + filename.split('_')[4]
    df['Season'] = season
    
    dfs.append(df)
    print(f"Processed: {filename}")

# Concatenate all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

# Save the merged dataframe to a new CSV file
output_file = 'all_nba_player_stats.csv'
merged_df.to_csv(output_file, index=False)

print(f"Successfully merged {len(csv_files)} CSV files into {output_file}")
print(f"Total rows in the merged file: {len(merged_df)}") 