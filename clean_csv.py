import csv
import pandas as pd
import re
import numpy as np
import os

# Increase the CSV field size limit
csv.field_size_limit(10000000)

def load_and_display_csv_from_directory(directory_path):
    # Loop through all files in the given directory
    for file_name in os.listdir(directory_path):
        # Check if the file is a CSV file
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)

            # Display the file name
            print(f"\n--- Data from: {file_name} ---")
            
            # Load the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)
            
            # Display the data types of each column
            print("\nData Types:")
            print(df.dtypes)
            
            # Display the first 5 rows of the DataFrame
            print("\nFirst 5 Rows:")
            print(df.head())

def safe_load_csv(file_path):
    cleaned_rows = []
    
    # Open the CSV with the built-in csv module to handle errors
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cleaned_rows.append(row)

    # Create a pandas DataFrame from the cleaned data
    df = pd.DataFrame(cleaned_rows[1:], columns=cleaned_rows[0])  # First row as headers
    return df

# Function to count URLs in the 'body' column
def count_urls_in_body(df):
    # Regular expression to match URLs
    url_pattern = r'(https?://\S+)'

    # Create a new column 'url_count' that counts URLs in each 'body' entry
    df['url_count'] = df['body'].apply(lambda x: len(re.findall(url_pattern, x)))

    return df

# Function to find if multiple data types exist in a given column
def find_multiple_data_types(df, column_name):
    # Apply type to each element in the column and get the unique types
    types_in_column = df[column_name].apply(type).unique()

    # Print the types found in the column
    print(f"Data types in column '{column_name}': {types_in_column}")

    # Check if there are multiple data types
    if len(types_in_column) > 1:
        print(f"Column '{column_name}' contains multiple data types.")
    else:
        print(f"Column '{column_name}' contains only one data type.")


file_path = './phishing_emails_merged.csv'
#df = safe_load_csv(file_path)
df = pd.read_csv(file_path)

print(df.dtypes)
print(df.head(100))
#df.to_csv(file_path, index=False)
df.head(100).to_csv('small.csv', index=False)
