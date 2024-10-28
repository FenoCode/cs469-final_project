import pandas as pd
import matplotlib.pyplot as plt

def plot_pii_over_time(time_series_df):
    """Plot readability scores over time with monthly bins."""
    plt.figure(figsize=(12, 6))

    plt.plot(time_series_df['date'], time_series_df['PII Count'], label='PII Count')
    # # Mark the release date of ChatGPT
    #chatgpt_release_date = '2022-11-30'  # Use the specific release date
    #plt.axvline(x=pd.to_datetime(chatgpt_release_date), color='red', linestyle='--', label='ChatGPT Release')
    
    plt.title('PII Occurrences Over Time')
    plt.xlabel('Date')
    plt.ylabel('Avg Occurrences in Email')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Load your DataFrame
file_path = './phishing_emails_pii_added.csv'
df = pd.read_csv(file_path)
df['date'] = pd.to_datetime(df['date'])
df = df[['date', 'PII Count']]

df.set_index('date', inplace=True)
df = df.resample('3M').mean().reset_index()

plot_pii_over_time(df)
