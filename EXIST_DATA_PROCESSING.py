import json
import csv
import re
import emoji
from wordsegment import load, segment
import unicodedata
# Load word segment data
load()
# Function to clean text
def clean_text(text):
    # Remove usernames
    text = re.sub(r'@[\w]+', '', text)
    # Convert to lowercase
    text = text.lower()
    # Replace emojis with their unicode description
    text = emoji.demojize(text)
    # Hashtag segmentation
    text = re.sub(r'#(\w+)', lambda m: ' '.join(segment(m.group(1))), text)
    # Remove links
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove unwanted '/'
    text = re.sub(r'/\s', '', text)
    # Remove punctuation except ' - / % & ... ¿ ?
    text = re.sub(r'[^\w\s\'%&¿?/-]', '', text)
    # Remove accented characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text
# Load JSON data
with open('/content/EXIST2023_training.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# Extract data and clean tweets
rows = []
for key in data:
    item = data[key]
    row = [
        item['id_EXIST'],
        item['lang'],
        clean_text(item['tweet']),
        item['number_annotators'],
        item['gender_annotators'],
        item['age_annotators'],
        item['labels_task1']
    ]
    rows.append(row)
# Write data to CSV
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['id_EXIST', 'lang', 'tweet', 'number_annotators', 'gender_annotators', 'age_annotators', 'labels_task1'])
    csvwriter.writerows(rows)