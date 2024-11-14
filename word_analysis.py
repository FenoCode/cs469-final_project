import re, nltk
from collections import Counter
from nltk.util import ngrams
import operator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#nltk.download('stopwords')
 
# we may not care about the usage of stop words
stop_words = nltk.corpus.stopwords.words('english') + [
 'ut', '\'re','.', ',', '--', '\'s', '?', ')', '(', ':', '\'',
 '\"', '-', '}', '{', '&', '|', u'\u2014', '', '+', 'Submission-ID',
 'I', 'The', 'To', 'This', 'A', 'If', 'You', 'From', '��', 'Aug',
 'No', 'We', 'may', 'Subject', 'It', 'said', 'Sender', 'THE', 'dont', 
 'Added', 'Submission', 'For', 'All', 'Sent', 'News', 'e-mail', 'In',
 'Message-----', '-----Original', 'Total', 'New', 'Im', 'Thanks', 'also',
 'US', 'On', 'Same', '#'
 ]

# We also want to remove special characters, quotes, etc. from each word
def cleanWord (w):
    # r in r'[.,"\']' tells to treat \ as a regular character 
    # but we need to escape ' with \'
    # any character between the brackets [] is to be removed 
    wn = re.sub('[,"\.\'&\|:@>*;/=]', "", w)
    # get rid of numbers
    return re.sub('^[0-9\.]*$', "", wn)

def get_wf(df):

    # Split words and clean each word in the DataFrame
    df['words'] = df['body'].str.split()
    df = df.explode('words')
    df['words'] = df['words'].apply(cleanWord)

    # Remove stop words and empty strings
    df = df[~df['words'].isin(stop_words) & df['words'].str.strip().astype(bool)]
    
    # Calculate word frequencies
    wf = df['words'].value_counts()
    
    # Convert the Series to a list of tuples and get the top 50 words
    wfs = wf.head(30).to_dict().items()
    
    # Calculate the total word count after cleaning
    total_words = wf.sum()
    
    return list(wfs), total_words

def plotWordCounts(wf, suptitle):
    # Sort the list in descending order by the count
    wf_sorted = sorted(wf, key=lambda x: x[1], reverse=True)
    
    # Create the figure
    f = plt.figure(figsize=(10, 6))
    f.suptitle(suptitle, fontsize=20)
    
    # Create the single subplot
    ax = f.add_subplot(111)
    pos = np.arange(len(wf_sorted)) 
    
    # Set the tick parameters
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_yticks(pos)
    ax.set_yticklabels([x[0] for x in wf_sorted])
    
    # Plot the bar chart
    ax.barh(pos, [x[1] for x in wf_sorted], align='center', color='skyblue')
    
    # Show the plot
    plt.show()

def trackWordOverTime(df, word, text_col='body', freq='D'):
    global start_date, end_date

    # Filter rows containing the word (case-insensitive)
    df['contains_word'] = df[text_col].str.contains(word, case=False, na=False)
    
    # Count occurrences of the word by date
    word_counts = df[df['contains_word']].groupby(pd.Grouper(key='date', freq=freq)).size()
    print(word_counts)
    
    # Plot word occurrences over time
    plt.figure(figsize=(10, 6))
    word_counts.plot(kind='line', marker='o', color='skyblue', linewidth=2)
    plt.title(f"Occurrences of '{word}' Over Time")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.xlim(pd.Timestamp(start_date), pd.Timestamp(end_date))
    plt.grid(True)
    plt.show()

def clean_word(word):
    """Remove special characters and make lowercase for uniformity."""
    return re.sub(r'[^\w\s]', '', word.lower())

def extract_common_phrases(df, target_words, window_size=3):
    """Extract common phrases around target words with a specified window size in a CSV file."""

    df['body'] = df['body'].fillna('').astype(str)

    phrase_counter = {word: Counter() for word in target_words}

    for text in df['body']:
        words = text.split()  # Tokenize each email body
        clean_words = [clean_word(word) for word in words]
        
        for i, word in enumerate(clean_words):
            if word in target_words:
                # Get context window around target word
                start = max(0, i - window_size)
                end = min(len(clean_words), i + window_size + 1)
                context_window = clean_words[start:end]
                
                # Create phrases (skip-grams) in the context window
                phrases = list(ngrams(context_window, len(context_window)))
                
                # Add phrases to the phrase counter for this target word
                for phrase in phrases:
                    phrase_counter[word][" ".join(phrase)] += 1

    return phrase_counter

# Data range globals
start_date = '2019-01-01'
end_date = '2024-12-31'

# Load the data, filter, and prepare the DataFrame at the top level
df = pd.read_csv('phishing_emails_features_added.csv', parse_dates=['date'])
df = df.query('label == 1')
df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]


# Now populate two lists    
(wf_ee, tw_ee) = get_wf(df)
print(wf_ee)

plotWordCounts(wf_ee, 'Word Count for Phishing Emails')
trackWordOverTime(df, 'email', freq='3M')
trackWordOverTime(df, 'account', freq='3M')
trackWordOverTime(df, 'information', freq='3M')

# Find context phrases around the top 3 occurring words
target_words = [key for key, _ in wf_ee[:3]]
print(target_words)
window_size = 5 # Context words surrouding the key word (phrase size)
phrase_counts = extract_common_phrases(df, target_words, window_size)

# Display the most common phrases for each target word
for word, phrases in phrase_counts.items():
    print(f"Common phrases around '{word}':")
    print(phrases.most_common(10))  # Display the 10 most common phrases
    print()