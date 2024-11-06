from transformers import pipeline, AutoTokenizer
import pandas as pd
import torch
import testparse as tp

# Function to split text into chunks of max tokens
def split_text_into_chunks(text, max_tokens):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        word_tokens = tokenizer.tokenize(word)
        word_length = len(word_tokens)

        # Check if adding this word exceeds max_tokens (after adding special tokens)
        if current_length + word_length + 1 > max_tokens:  # +1 for the [CLS] token
            if current_chunk:  # Avoid adding empty chunks
                chunks.append(" ".join(current_chunk))
            current_chunk = [word]  # Start a new chunk
            current_length = word_length  # Reset current length to the new word
        else:
            current_chunk.append(word)  # Add word to the current chunk
            current_length += word_length  # Update the current length

    # Add the last chunk if it exists and ensure it fits within limits
    if current_chunk:  
        if current_length + 1 <= max_tokens:  # Check for the [CLS] token
            chunks.append(" ".join(current_chunk))

    return chunks

# Classify each chunk, skipping any that cause an error
def classify_long_text(text, max_length=512):
    chunks = split_text_into_chunks(text, max_length)
    results = []
    
    for chunk in chunks:
        try:
            result = gen(chunk)
            results.append(result)
        except Exception as e:
            print(f"Skipping chunk due to error: {e}")
            continue
    
    return results

model_name = 'j-hartmann/emotion-english-distilroberta-base'
gen = pipeline("text-classification", model=model_name, device=0 if torch.cuda.is_available() else -1, return_all_scores=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)
max_tokens = tokenizer.model_max_length  # Get max token length for the model
max_tokens = max_tokens - 64 # Reduced max size for saftey

file_path = './phishing_email_pii_added.csv'
df = pd.read_csv(file_path)
df = df.dropna()

# Filter by date range
start_date = '1995-01-01'
end_date = '2022-12-31'
df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Process each email body and classify
r = []
for index, row in df.iterrows():
    # Initialize label scores to 0
    label_scores = {}
    for label in ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness','surprise']:  # Adjust based on actual model labels
        label_scores[label] = []
    
    text = row['body']  # Get the body of the current email
    results = classify_long_text(text, max_tokens)
    
    for result in results:
        for classes in result:
            for label_class in classes:
                label_scores[label_class['label']].append(label_class['score'])

    # Average scores across chunks for each label
    avg_label_scores = {label: (sum(scores) / len(scores)) if scores else 0 for label, scores in label_scores.items()}

    # Select the label with the highest average score
    final_label = max(avg_label_scores, key=avg_label_scores.get)
    r.append(final_label)

# Insert results into the dataframe
df.insert(df.shape[1], "Emotion", r, True)
print(df)
df = df[['body', 'Emotion']]
df.to_csv("./test.csv", index=False)