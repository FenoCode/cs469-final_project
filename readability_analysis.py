import pandas as pd
import textstat
import matplotlib.pyplot as plt
import testparse

def calculate_readability_scores(text):
    """Calculate readability scores for a given text."""
    return {
        #'Flesch-Kincaid': textstat.flesch_kincaid_grade(text),
        #'Gunning Fog': textstat.gunning_fog(text),
        #'Flesch Reading Ease': textstat.flesch_reading_ease(text),
        'SMOG Index': textstat.smog_index(text),
        #'Automated Readability Index': textstat.automated_readability_index(text),
        #'Coleman Liau' : textstat.coleman_liau_index(text),
        #'Linsear Write Formula' : textstat.linsear_write_formula(text),
        #'Reading Time (ms)' : textstat.reading_time(text)
    }

def analyze_phishing_emails(df):
    """Analyze phishing emails for readability scores over time, grouped by month."""
    # Assume df has columns 'date' and 'email_content'
    df['readability_scores'] = df['body'].apply(calculate_readability_scores)
    
    # Normalize readability scores into separate columns
    readability_df = df['readability_scores'].apply(pd.Series)
    
    # Combine with original dataframe
    analysis_df = pd.concat([df[['date']], readability_df], axis=1)
    
    # Resample by month and calculate average readability scores
    analysis_df['date'] = pd.to_datetime(analysis_df['date'])
    analysis_df.set_index('date', inplace=True)
    monthly_avg_df = analysis_df.resample('M').mean().reset_index()
    
    return monthly_avg_df

def plot_readability_over_time(time_series_df):
    """Plot readability scores over time with monthly bins."""
    plt.figure(figsize=(12, 6))
    for column in time_series_df.columns[1:]:
        plt.plot(time_series_df['date'], time_series_df[column], label=column)
    
    plt.title('Readability Scores of Phishing Emails (Monthly Average)', fontsize=24)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Readability Score', fontsize=16)
    # plt.title('Reading Time (Historical Average)', fontsize=24)
    # plt.xlabel('Date', fontsize=16)
    # plt.ylabel('Time (Seconds)', fontsize=16)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Load your dataset here
    # Example: df = pd.read_csv('phishing_emails.csv')
    # Ensure your DataFrame has 'date' and 'body' columns.
    
    
    # Step 1: Read in dataset and do initial dataset cleanup
    file_path = './phishing_emails_merged_filtered.csv'
    #df = safe_load_csv(file_path)
    df = pd.read_csv(file_path)
    df = df.dropna()
    df = df.query('label == 1')
    #df['body'] = df['body'].apply(testparse.preprocess_email_content)
    print("Done parsing")
    # Step 2: Filter rows between 1995 and 2013 (inclusive)
    start_date = '1995-01-01'
    end_date = '2022-12-31'
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    # Sort and grab top values
    #df = df.sort_values(by='parsed_date',ascending=True)
    #df = df.head(100000)
    
    # Analyze the phishing emails
    time_series_df = analyze_phishing_emails(df)

    # Plot the results
    plot_readability_over_time(time_series_df)