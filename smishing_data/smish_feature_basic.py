import re
import pandas as pd

# Got code snippets from https://data.mendeley.com/datasets/f45bkkt8pr/1

emailPattern = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`" "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|" "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
phonePattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')

def email_check(line):
    if emailPattern.search(line) is not None:
        return 1
    else:
        return 0

def phoneNumber_check(line):
    if phonePattern.search(line) is not None:
        return 1
    else:
        return 0
    
def http_check(line):
    http = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
    if not http:
        return 0
    else:
        return 1
    
df = pd.read_csv('./smishing_data/sms-phishing-subset.csv')
df = df.dropna()

email_label =[]
phone_label =[]
http_label =[]
for i, row in df.iterrows():
    #print(row)
    if(email_check(row.body)):
        email_label.append("Yes")
    else:
        email_label.append("No")

    if(phoneNumber_check(row.body)):
        phone_label.append("Yes")
    else:
        phone_label.append("No")
    
    if(http_check(row.body)):
        http_label.append("Yes")
    else:
        http_label.append("No")   

df['URL'] = http_label 
df['EMAIL'] = email_label
df['PHONE'] = phone_label

df.to_csv('./smishing_data/sms-phishing-subset-features.csv', index=False)