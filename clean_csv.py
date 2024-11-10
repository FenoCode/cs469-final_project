import csv
import pandas as pd

csv.field_size_limit(10000000)  # Make CSV field size arbitrarily large.
input_file_path = './phishing_emails_merged.csv'            # Input file path to load unparsed dataset.
output_file_path = './phishing_emails_merged_filtered.csv'  # Output file path with new parsed dataset.
debug_print = True             # Prints debugging information.
output_file = True              # Outputs new parsed dataset.

# Main function.
if __name__ == "__main__":
    df = pd.read_csv(input_file_path)

    if debug_print:
        print(df.dtypes)
        print(df)

    if not output_file:
        exit()

    # Apply type to each element in the column and get the unique types.
    for column in df.columns.tolist():

        types_in_column = df[column].apply(type).unique()
        if debug_print:
            # Print the types found in the column.
            print(f"Data types in column '{column}': {types_in_column}")

            # Check if there are multiple data types.
            if len(types_in_column) > 1:
                print(f"Column {column} contains multiple data types.")
            else:
                print(f"Column {column} contains only one data type.")

    # Fill NaN values with empty strings to avoid 'float' conversion errors.
    df = df.fillna('')

    # Try to convert the 'date' column to datetime.
    df['parsed_date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)

    # Find rows where the date could not be parsed.
    unparseable_dates = df[df['parsed_date'].isna()]['date']

    if debug_print:
        # Display results.
        print("Unparseable Dates:")
        print(pd.DataFrame({'Date': unparseable_dates}))

        # Output the original DataFrame with parsed dates.
        print("\nOriginal DataFrame with Parsed Dates:")
        print(df)

    # Step 3: Drop the unparseable dates.
    df['date'] = df['parsed_date']
    df = df.drop(columns=['parsed_date'])

    # Step 4: Drop any column with NaN values in the text fields
    df = df.dropna()
    
    df.to_csv(output_file_path, index=False)