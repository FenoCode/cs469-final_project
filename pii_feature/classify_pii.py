from transformers import pipeline, AutoConfig
import os
import pandas as pd

pii_categories = [
    'FIRSTNAME', 
    'LASTNAME', 
    'EMAIL', 
    'PHONE_NUMBER', 
    'USERNAME', 
    'JOBTITLE', 
    'COMPANY_NAME', 
    'ACCOUNTNUMBER', 
    'ACCOUNTNAME', 
    'IBAN', 
    'CREDITCARDNUMBER', 
    'CREDITCARDCVV', 
    'STREETADDRESS', 
    'CITY', 
    'ZIPCODE', 
    'STATE', 
    'SSN', 
    'PASSWORD', 
    'URL', 
    'IP', 
    'USERAGENT', 
    'SEX', 
    'GENDER' 
]

class_threshold = .90
model_name = 'lakshyakh93/deberta_finetuned_pii'
gen = pipeline("token-classification", model_name, device=0)  # Ensure GPU is enabled

file_path = './phishing_emails_merged_filtered.csv'
df = pd.read_csv(file_path)
df = df.dropna()


batch_size = 1024  # Adjust batch size based on GPU memory

# Generate PII statistics about each email in batches
results = []
for i in range(0, len(df), batch_size):
    batch = df['body'][i:i + batch_size].tolist()
    outputs = gen(batch, aggregation_strategy="first")
    
    for j, output in enumerate(outputs):
        pii_count = sum(1 for pii in output if pii['score'] > class_threshold and pii['entity_group'] in pii_categories)
        date = df.iloc[i + j]['date']
        results.append(pii_count)

df.insert(df.shape[1], "PII Count", results, True)
print(df)
df.to_csv("./phishing_email_pii_added.csv")