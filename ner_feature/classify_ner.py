import torch
from transformers import pipeline, AutoConfig, AutoTokenizer, AutoModelForTokenClassification
import os
import pandas as pd

class_threshold = .95
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")


nlp = pipeline("ner", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

file_path = './phishing_emails_merged_filtered.csv'
df = pd.read_csv(file_path)
df = df.dropna()

batch_size = 1024  # Adjust batch size based on GPU memory

# Generate NER statistics about each email in batches
results = []
for i in range(0, len(df), batch_size):
    batch = df['body'][i:i + batch_size].tolist()
    outputs = nlp(batch, aggregation_strategy="first")
    
    for j, output in enumerate(outputs):
        ner_count = sum(1 for pii in output if pii['score'] > class_threshold)
        date = df.iloc[i + j]['date']
        results.append(ner_count)

df.insert(df.shape[1], "NER Count", results, True)
print(df)
df.to_csv("./phishing_emails_ner_added.csv", index=False)