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

class_threshold = .95
model_name = 'lakshyakh93/deberta_finetuned_pii'
gen = pipeline("token-classification", model_name, device=-1)

file_path = './phishing_emails_merged_filtered.csv'
#df = safe_load_csv(file_path)
df = pd.read_csv(file_path)
df_small = df.head(10)
del df

for body in df_small['body']:
    output = gen(body, aggregation_strategy="first")
    for  pii in output:
        if pii['score'] > class_threshold:
            if pii['entity_group'] in pii_categories:
                print(pii)
    print('\n\n')