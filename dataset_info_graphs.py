import pandas as pd
import matplotlib.pyplot as plt

# Sample data loading
# Replace this with your actual dataset
# Assuming `df` has 'date' and 'label' columns
df = pd.read_csv("./phishing_emails_features_added.csv")
df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' is in datetime format

start_date = '1995-01-01'
end_date = '2024-12-31'
df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Extract year from date
df['year'] = df['date'].dt.year

# Total counts of phishing vs. non-phishing emails
total_counts = df['label'].value_counts()

# Group by year and label, then count occurrences
yearly_distribution = df.groupby(['year', 'label']).size().unstack(fill_value=0)

# Calculate percentage breakdown by year
yearly_distribution_percent = yearly_distribution.div(yearly_distribution.sum(axis=1), axis=0) * 100

# Set up the figure with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 12), gridspec_kw={'width_ratios': [1, 2]})

# First plot: Total phishing vs. non-phishing in the dataset
total_counts.plot(kind='pie', labels=['Non-Phishing (0)', 'Phishing (1)'], autopct='%1.1f%%', colors=['skyblue', 'salmon'], ax=ax1, fontsize=16)
ax1.set_title("Total Phishing vs Non-Phishing Emails in Dataset", fontsize=18)
ax1.set_ylabel('')  # Hide y-label for a cleaner look

# Second plot: Percentage distribution by year
yearly_distribution_percent.plot(kind='bar', stacked=True, ax=ax2, color=['skyblue', 'salmon'])
ax2.set_title("Yearly Phishing vs Non-Phishing Distribution", fontsize=18)
ax2.set_xlabel("Year", fontsize=14)
ax2.set_ylabel("% of Emails", fontsize=14)
ax2.legend(["Non-Phishing (0)", "Phishing (1)"], fontsize=12)
ax2.tick_params(axis='x', rotation=45)

# Improve layout
plt.tight_layout()
plt.show()