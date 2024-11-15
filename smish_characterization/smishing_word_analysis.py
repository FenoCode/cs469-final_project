import re, nltk
from collections import Counter
from nltk.util import ngrams
import operator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

def get_wf(df, top_words):

    # Split words and clean each word in the DataFrame
    df['words'] = df['body'].str.split()
    df = df.explode('words')
    df['words'] = df['words'].apply(cleanWord)

    # Remove stop words and empty strings
    df = df[~df['words'].isin(stop_words) & df['words'].str.strip().astype(bool)]
    
    # Calculate word frequencies
    wf = df['words'].value_counts()
    
    # Convert the Series to a list of tuples and get the top 50 words
    wfs = wf.head(top_words).to_dict().items()
    
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

def trackWordsOverTime(df, words, text_col='body', freq='D'):
    global start_date, end_date
    
    # Initialize the plot
    plt.figure(figsize=(10, 6))
    
    # Split words and clean each word in the DataFrame
    df['words'] = df[text_col].str.split()
    df = df.explode('words')
    df['words'] = df['words'].apply(cleanWord)
    
    # Loop over each word, filter for occurrences, and plot
    for word in words:
        # Filter rows containing the word (case-insensitive)
        df['contains_word'] = df['words'].str.contains(word, case=False, na=False)
        
        # Count occurrences of the word by date
        word_counts = df[df['contains_word']].groupby(pd.Grouper(key='date', freq=freq)).size()
        
        # Plot word occurrences over time with a unique color for each word
        word_counts.plot(kind='line', marker='o', linewidth=2, label=word)

    # Add title, labels, and legend
    plt.title("Occurrences of Words Over Time")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.xlim(pd.Timestamp(start_date), pd.Timestamp(end_date))
    plt.legend(title="Words")
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
df = pd.read_csv('./smishing_data/sms-phishing-subset-features.csv')
df = df.query('label == "smish" or label == "spam"')
#df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Calculate word frequency in emails   
(wf_ee, tw_ee) = get_wf(df, top_words=20)
print(wf_ee)
plotWordCounts(wf_ee, 'Word Count for Smishing Messages')

# Get top N words to analyze
num_targets = 7
target_words = [key for key, _ in wf_ee[:num_targets]]
print(target_words)

# Plot occurences over time
#trackWordsOverTime(df, target_words, freq='3ME')

# Find context phrases around the top N occurring words
window_size = 3 # Context words surrouding the key word (phrase size)
num_phrases = 3
phrase_counts = extract_common_phrases(df, target_words, window_size)
phrase_count_data = []
# Display the most common phrases for each target word
for word, phrases in phrase_counts.items():
    print(f"Common phrases around '{word}':")
    phrase_lst = phrases.most_common(num_phrases) # Display the N most common phrases
    print(phrase_lst)
    print()
    # Transforming Counter() data for future data visualization
    for phrase in phrase_lst: 
        phrase_count_data.append( (word, phrase[0], phrase[1]))

# Generate word cloud and plot alongside the most commonly occuring phrases
df_phrases = pd.DataFrame(phrase_count_data, columns=['Word', 'Phrase', 'Frequency'])

# Set up figure and axes for the word cloud and table side-by-side
fig, axs = plt.subplots(1, 2, figsize=(14, 7))

# Generate and plot the word cloud
wf_ee = dict(wf_ee)
wordcloud = WordCloud(width=600, height=400, background_color='white').generate_from_frequencies(wf_ee)
axs[0].imshow(wordcloud, interpolation='bilinear')
axs[0].axis('off')
axs[0].set_title("Most Frequent Words in Emails")

# Create the phrase table as a bar chart with labels for each word
# Get top phrases for each word
top_phrases = df_phrases.groupby('Word').apply(lambda x: x.nlargest(num_phrases, 'Frequency')).reset_index(drop=True)
phrases = top_phrases['Phrase']
frequencies = top_phrases['Frequency']
words = top_phrases['Word']

# Plot bars with phrases as y-tick labels
colors = ['skyblue'] * num_phrases +  ['lightgreen'] * num_phrases +  ['salmon'] * num_phrases + ['peachpuff'] * num_phrases + ['plum'] * num_phrases
axs[1].barh(phrases, frequencies, color=colors)
axs[1].invert_yaxis()  # Display the highest frequency at the top
axs[1].set_xlabel("Frequency")
axs[1].set_title("Most Common Phrases Around Keywords")

# Annotate bars with the associated keyword
for index, (freq, word) in enumerate(zip(frequencies, words)):
    axs[1].text(freq + 1, index, word, va='center', ha='left', color='black', fontweight='bold')

plt.tight_layout()
plt.show()