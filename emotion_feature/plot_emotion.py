import pandas as pd
import matplotlib.pyplot as plt

# Sample data loading
# Replace this with your actual dataset
# Assuming `df` has 'date' and 'label' columns
df = pd.read_csv("./phishing_email_pii_emotion_added_phishing.csv")
df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' is in datetime format

# Extract year from date
df['year'] = df['date'].dt.year

# Total counts of phishing 
df = df[df['label'] == 1]
total_counts = df['Emotion'].value_counts()

# Group by year and label, then count occurrences
yearly_distribution = df.groupby(['year', 'Emotion']).size().unstack(fill_value=0)

# Calculate percentage breakdown by year
yearly_distribution_percent = yearly_distribution.div(yearly_distribution.sum(axis=1), axis=0) * 100
print(yearly_distribution_percent)

# Set up the figure with subplots
# First plot: Total phishing vs. non-phishing in the dataset
colors = ['skyblue', 'salmon', 'lightgreen', 'peachpuff', 'lightgrey', 'plum', 'khaki']
# Set up the figure with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 12), gridspec_kw={'width_ratios': [1, 2]})

# Sort the total_counts by occurrences (in descending order)
sorted_total_counts = total_counts.sort_values(ascending=False)
print(sorted_total_counts)


# Prepare data for the pie chart
sizes = sorted_total_counts.values  # Values for the pie slices
labels = sorted_total_counts.index  # Labels based on the sorted total_counts
sorted_labels = labels.sort_values()
sorted_colors = []

# Matches colors for the first and 2nd plots
for label in sorted_labels:
    print(label)
    sorted_colors.append(colors[labels.get_loc(label)])


# Create pie chart with custom colors in ax1
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)

# Set the title for ax1
ax1.set_title("Total Emotional Sentiment Distribution (Phishing Emails)")
ax1.set_ylabel('')  # Hide y-label for a cleaner look

# The second plot (e.g., bar chart) will go on ax2 as before
yearly_distribution_percent.plot(kind='bar', stacked=True, color=sorted_colors, ax=ax2)
ax2.set_title("Emotional Sentiment Distribution by Year (Phishing Emails)")
ax2.set_xlabel("Year")
ax2.set_ylabel("Percentage of Emails")
ax2.tick_params(axis='x', rotation=45)

# Improve layout
plt.tight_layout()
plt.show()