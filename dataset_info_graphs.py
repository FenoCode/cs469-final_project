import pandas as pd
import matplotlib.pyplot as plt

# Sample data loading
# Replace this with your actual dataset
# Assuming `df` has 'date' and 'label' columns
df = pd.read_csv("./phishing_email_pii_added.csv")
df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' is in datetime format

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
total_counts.plot(kind='pie', labels=['Non-Phishing (0)', 'Phishing (1)'], autopct='%1.1f%%', colors=['skyblue', 'salmon'], ax=ax1)
ax1.set_title("Total Phishing vs Non-Phishing Emails in Dataset")
ax1.set_ylabel('')  # Hide y-label for a cleaner look

# Second plot: Percentage distribution by year
yearly_distribution_percent.plot(kind='bar', stacked=True, ax=ax2, color=['skyblue', 'salmon'])
ax2.set_title("Percentage Distribution of Phishing vs Non-Phishing Emails by Year")
ax2.set_xlabel("Year")
ax2.set_ylabel("Percentage of Emails")
ax2.legend(["Non-Phishing (0)", "Phishing (1)"])
ax2.tick_params(axis='x', rotation=45)

# Improve layout
plt.tight_layout()
plt.show()