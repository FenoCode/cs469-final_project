import pandas as pd
import sys
sys.path.append("./")
import testparse as tp

# Prepare 1st file - SMSSmishCollection.txt
f = open('./smishing_data/SMSSmishCollection.txt', 'r')
text = f.readlines()
labels = []
messages = []
for line in text:
    # Parse text file for labels and body text
    words = line.split()
    label = words[0]
    body =  ' '.join(words[1:])

    labels.append(label)
    messages.append(body)


df1 = pd.DataFrame({'body': messages, 'label': labels})
df1['body'] = df1['body'].apply(tp.remove_special_characters)
df1['body'] = df1['body'].apply(tp.remove_excess_whitespace)
df1 = df1.dropna()
#df1.to_csv('./smishing_data/SMSSmishCollection.csv', index=False)
print(df1)

# Prepare 2nd file - smishtank.csv - from SmishTank
df2 = pd.read_csv("./smishing_data/smishtank.csv", encoding='latin1')

df2 = df2[['MainText']]
df2['body'] = df2['MainText']
df2 = df2.drop(columns=['MainText'])

labels =[]
for i, row in df2.iterrows():
    # All rows from the SmishTank dataset are confirmed smishing messages
    labels.append("smish")

df2['label'] = labels
#df2.to_csv("./smishing_data/smishtank-subset.csv", encoding='utf-8', index=False)
print(df2)

# Prepare 3rd file - Dataset_5971.csv
df3 = pd.read_csv("./smishing_data/Dataset_5971.csv")
df3 = df3[['TEXT','LABEL']]
df3['body'] = df3['TEXT']
df3['label'] = df3['LABEL']
df3 = df3.drop(columns=['TEXT', 'LABEL'])

# Combine all files and normalize labels
df = pd.concat([df1, df2, df3])

def normalize_labels(label):
    label = label.lower()
    if (label == 'smishing'):
        return 'smish'
    return label

df['label'] = df['label'].apply(normalize_labels)

df.to_csv("./smishing_data/sms-phishing-subset.csv", index=False, encoding='utf-8')
print("FINAL OUTPUT:")
print(df)
print("\nLabels:")
print(df['label'].unique())

