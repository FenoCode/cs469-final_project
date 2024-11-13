import pandas as pd
import matplotlib.pyplot as plt

def plot_pii_over_time(time_series_df):
    """Plot readability scores over time with monthly bins."""
    plt.figure(figsize=(12, 6))

    plt.plot(time_series_df['date'], time_series_df['NER Count'], label='NER Count')
    # # Mark the release date of ChatGPT
    #chatgpt_release_date = '2022-11-30'  # Use the specific release date
    #plt.axvline(x=pd.to_datetime(chatgpt_release_date), color='red', linestyle='--', label='ChatGPT Release')
    
    plt.title('NER Occurrences Over Time')
    plt.xlabel('Date')
    plt.ylabel('Avg Occurrences in Email')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Load your DataFrame
file_path = './phishing_emails_features_added.csv'
df = pd.read_csv(file_path)
df['date'] = pd.to_datetime(df['date'])
df = df[['date', 'label', 'NER Count']]

# Step 2: Filter rows between 1995 and 2013 (inclusive)
start_date = '1995-01-01'
end_date = '2008-12-31'
df_early = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
df_early.set_index('date', inplace=True)

plt.figure(figsize=(12, 6))

# Plotting spam vs non-spam data
df_ham = df_early.query('label == 0')
df_ham = df_ham.resample('3M').mean().reset_index()
plt.plot(df_ham['date'], df_ham['NER Count'], label='Non-Phishing')

df_spam = df_early.query('label == 1')
df_spam = df_spam.resample('3M').mean().reset_index()
plt.plot(df_spam['date'], df_spam['NER Count'], label='Phishing')
# # Mark the release date of ChatGPT
#chatgpt_release_date = '2022-11-30'  # Use the specific release date
#plt.axvline(x=pd.to_datetime(chatgpt_release_date), color='red', linestyle='--', label='ChatGPT Release')

plt.title('NER Occurrences Over Time')
plt.xlabel('Date')
plt.ylabel('Avg Occurrences in Email')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()

plt.figure(figsize=(12, 6))

start_date = '2008-12-31'
end_date = '2024-12-31'
df_late = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
df_late.set_index('date', inplace=True)
df_late = df_late.resample('3M').mean().reset_index()
plt.plot(df_late['date'], df_late['NER Count'], label='Phishing')
plt.title('NER Occurrences Over Time')
plt.xlabel('Date')
plt.ylabel('Avg Occurrences in Email')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()