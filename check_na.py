import pandas as pd

# Load the CSV file
df = pd.read_csv('tagged_videos4.csv')

# Count rows with NaN values in 'tags'
nan_count = df['tags'].isna().sum()

# Count rows where 'tags' is exactly "N/A"
na_value_count = (df['tags'] == "N/A").sum()

no_trans_value_count = (df['tags'] == "No Transcript").sum()
no_trans_value_count2 = ((df['tags'] != "No Transcript") & df['transcript'].isna()).sum()


print(f"Rows with NaN in 'tags': {nan_count}")
print(f"Rows with 'N/A' in 'tags': {na_value_count}")
print(f"Rows with 'No Transcript' in 'tags': {no_trans_value_count}")
print(f"not yet' in 'tags': {no_trans_value_count2}")
