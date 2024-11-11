import re, nltk
from collections import Counter
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
""""
# define a function to get text/clean/calculate frequency
def get_wf (file):
    f = open(file, 'r', encoding="ascii", errors='replace')
    t = f.read()
    
    # obtain words by splitting a string using as separator one or more (+) space/like characters (\s) 
    wds = re.split('\s+',t)
    
    # remove periods, commas, etc stuck to the edges of words
    for i in range(len(wds)):
        wds[i] = cleanWord(wds [i])
    
    # now populate a dictionary (wf)
    wf = Counter (wds)
    
    # Remove stop words from the dictionary wf
    for k in stop_words:
        wf. pop(k, None)
    
    # Word count
    tw = 0
    for w in wf:
       tw += wf[w] 
        
    # Get ordered list
    wfs = sorted (wf.items(), key = operator.itemgetter(1), reverse=True)
    ml = min(len(wfs),50)

    # Reverse the list because barh plots items from the bottom
    return (wfs [ 0:ml ] [::-1], tw)
"""
def get_wf(file):
    global start_date, end_date
    # Load the file content into a DataFrame for easier manipulation
    df = pd.read_csv(file, parse_dates=['date'])

    # Filter dataframe based on provided date range
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Split words and clean each word in the DataFrame
    df['words'] = df['body'].str.split()
    df = df.explode('words')
    df['words'] = df['words'].apply(cleanWord)

    # Remove stop words and empty strings
    df = df[~df['words'].isin(stop_words) & df['words'].str.strip().astype(bool)]
    
    # Calculate word frequencies
    wf = df['words'].value_counts()
    
    # Convert the Series to a list of tuples and get the top 50 words
    wfs = wf.head(50).to_dict().items()
    
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

def trackWordOverTime(csv_file, word, text_col='body', freq='D'):
    global start_date, end_date
    # Load CSV file
    df = pd.read_csv(csv_file, parse_dates=['date'])

    # Filter dataframe based on provided date range
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

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
        
# Data range globals
start_date = '2019-01-01'
end_date = '2024-12-31'

# Now populate two lists    
(wf_ee, tw_ee) = get_wf('phishing_emails_merged_filtered.csv')
print(wf_ee)

plotWordCounts(wf_ee, 'Word Count for Phishing Emails')
trackWordOverTime('phishing_emails_merged_filtered.csv', 'email', freq='3M')
