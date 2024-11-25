import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Step 1: Load the data
df = pd.read_csv('./phishing_emails_features_added_test.csv')

# Step 1.5: Balance the data to have equal number of phishing vs non-phishing
min_count = df['label'].value_counts().min()
df = df.groupby('label').apply(lambda x: x.sample(n=min_count, random_state=42)).reset_index(drop=True)


# Verify the distribution after balancing
print("Balanced label distribution:")
print(df['label'].value_counts())

# Step 2: Label Distribution Analysis
label_counts = df['label'].value_counts()
plt.figure(figsize=(8, 4))
sns.barplot(x=label_counts.index, y=label_counts.values, palette="viridis")
plt.title("Label Distribution")
plt.xlabel("Label")
plt.ylabel("Frequency")
plt.show()

# Step 3: Correlation Analysis - Convert Yes/No to Binary (1/0) for Analysis
df['URL'] = df['URL'].map({'Yes': 1, 'No': 0})
df['EMAIL'] = df['EMAIL'].map({'Yes': 1, 'No': 0})
df['PHONE'] = df['PHONE'].map({'Yes': 1, 'No': 0})
#df['label'] = df['label'].map({'smish': 1, 'spam': 1, 'ham': 0})

# Step 4: Correlation Heatmap
correlation_matrix = df[['label', 'URL', 'EMAIL', 'PHONE']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix between Features and Label")
plt.show()

# Step 5: Chi-square Tests for Independence
def chi_square_test(column):
    contingency_table = pd.crosstab(df['label'], df[column])
    chi2, p, dof, ex = chi2_contingency(contingency_table)
    return p

p_values = {col: chi_square_test(col) for col in ['URL', 'EMAIL', 'PHONE']}
print("Chi-square p-values for feature independence tests:")
print(p_values)

# Step 6: Visualizations for Feature Presence by Label
features = ['URL', 'EMAIL', 'PHONE']
fig, axs = plt.subplots(1, 3, figsize=(14, 7))
for i, feature in enumerate(features):
    countplot = sns.countplot(x=feature, hue='label', data=df, palette="viridis", ax=axs[i])
    axs[i].set_title(f"Presence of {feature} by Label", fontsize=18)
    axs[i].set_xlabel(f"{feature} Presence", fontsize=16)
    axs[i].set_ylabel("Count", fontsize=16)
    axs[i].tick_params(axis='x', labelsize=14)
    axs[i].tick_params(axis='y', labelsize=14)
    axs[i].legend(title="Label", loc="upper right", labels=["non-phishing", "phishing"],fontsize=14)

plt.show()


# Total count of each label
label_counts = df['label'].value_counts(normalize=True)

# Helper function to calculate conditional probability
def conditional_probability(df, label, conditions):
    subset = df
    for feature, value in conditions.items():
        subset = subset[subset[feature] == value]
    
    # Avoid zero division: only calculate if subset is not empty
    if len(subset) == 0:
        return 0  # No data matches this condition
    # Calculate P(label | conditions) = count of subset with label / total count of subset
    return len(subset[subset['label'] == label]) / len(subset)

# Evaluates all combinations of labels to find statistical significance 
combinations = [
    {'PHONE': 0, 'EMAIL': 0, 'URL': 0},   
    {'PHONE': 0, 'EMAIL': 0, 'URL': 1},
    {'PHONE': 0, 'EMAIL': 1, 'URL': 0},
    {'PHONE': 0, 'EMAIL': 1, 'URL': 1},
    {'PHONE': 1, 'EMAIL': 0, 'URL': 0},
    {'PHONE': 1, 'EMAIL': 0, 'URL': 1},
    {'PHONE': 1, 'EMAIL': 1, 'URL': 0},
    {'PHONE': 1, 'EMAIL': 1, 'URL': 1},
]

smish_dataset_probability = []
for combo in combinations:
    p_ham = conditional_probability(df, 0, combo)
    p_smish_spam = conditional_probability(df, 1, combo)
    confidence_ham = p_ham / (p_ham + p_smish_spam)
    confidence_smish_spam = p_smish_spam / (p_ham + p_smish_spam)

    
    print(f"\nFor conditions {combo}:")
    print(f"Probability of 'ham': {p_ham:.2%}")
    print(f"Confidence of 'ham': {confidence_ham:.2%}")
    print(f"Probability of 'smish/spam': {p_smish_spam:.2%}")
    print(f"Confidence of 'smish/spam': {confidence_smish_spam:.2%}")
    smish_dataset_probability.append({'PHONE': combo['PHONE'], 
                                      'EMAIL': combo['EMAIL'],
                                      'URL' : combo['URL'],
                                      'ham_prob': p_ham, 'ham_conf' : confidence_ham,
                                       'smish_spam_prob' : p_smish_spam, 'smish_spam_conf' : confidence_smish_spam})
    
# Visualize probabilities
df_prob = pd.DataFrame(smish_dataset_probability)

# Pivot tables for heatmaps
ham_conf_matrix = df_prob.pivot_table(index='PHONE', columns=['EMAIL', 'URL'], values='ham_conf')
smish_spam_conf_matrix = df_prob.pivot_table(index='PHONE', columns=['EMAIL', 'URL'], values='smish_spam_conf')

# Plot heatmaps
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.heatmap(ham_conf_matrix, annot=True, fmt=".2f", cmap="Blues", ax=axes[0])
axes[0].set_title('Confidence for Non-Phishing')
axes[0].set_xlabel('EMAIL, URL')
axes[0].set_ylabel('PHONE')

sns.heatmap(smish_spam_conf_matrix, annot=True, fmt=".2f", cmap="Reds", ax=axes[1])
axes[1].set_title('Confidence for Phishing')
axes[1].set_xlabel('EMAIL, URL')
axes[1].set_ylabel('PHONE')

plt.tight_layout()
plt.show()
