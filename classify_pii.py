from transformers import pipeline
import os
import pandas as pd

gen = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii", device=-1)

file_path = './phishing_emails_merged_filtered.csv'
#df = safe_load_csv(file_path)
df = pd.read_csv(file_path)
df_small = df.head(2)
del df

for body in df_small['body']:
    output = gen(body, aggregation_strategy="first")
    print(output)
    print('\n\n')