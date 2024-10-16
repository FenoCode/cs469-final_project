import pandas as pd
import os

# Main function.
if __name__ == "__main__":
    directory_path = os.path.join(os.getcwd(), 'phishing_data')
    merged_df = pd.DataFrame()
    error_messages = []

    # Iterate over all CSV files in the directory.
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            try:
                print(file_path)

                # Read the CSV file.
                df = pd.read_csv(file_path)
                
                # Check for column mismatches if merged_df is not empty.
                if not merged_df.empty:

                    # Skip this file if there is a mismatch.
                    if set(df.columns) != set(merged_df.columns):
                        error_messages.append(f"Column mismatch in file: {filename}. Expected columns: {list(merged_df.columns)}, found columns: {list(df.columns)}")
                        continue

                # Merge the DataFrame (outer join to include all data).
                merged_df = pd.concat([merged_df, df], ignore_index=True)

            except Exception as e:
                error_messages.append(f"Error reading {filename}: {str(e)}")

    # Display the final merged DataFrame.
    print("Final Merged DataFrame:")
    merged_df.to_csv('phishing_emails_merged.csv', index=False)

    # Output error messages if any.
    if error_messages:
        print("\nErrors encountered during processing:")
        for message in error_messages:
            print(message)
    else:
        print("\nNo errors encountered.")