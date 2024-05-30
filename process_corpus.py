import json
import pymorphy2
import re
import nltk
from nltk.tokenize import word_tokenize
from tqdm import tqdm

nltk.download('punkt')

def clean_text(text):
    text = re.sub(r'[^а-яА-ЯёЁ\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_text(text, morph):
    cleaned_text = clean_text(text)
    tokens = word_tokenize(cleaned_text)
    result = []
    for token in tokens:
        parsed_word = morph.parse(token)[0]
        lemma = parsed_word.normal_form
        tag = parsed_word.tag
        result.append({
            'token': token,
            'lemma': lemma,
            'POS': tag.POS,
            'case': tag.case,
            'number': tag.number,
            'gender': tag.gender,
            'tense': tag.tense,
            'aspect': tag.aspect,
            'mood': tag.mood,
            'voice': tag.voice,
            'person': tag.person
        })
    return result

def process_data(data):
    morph = pymorphy2.MorphAnalyzer()
    for entry in tqdm(data, desc="Processing texts"):
        entry['processed_text'] = process_text(entry['text'], morph)
    return data

def main():
    input_file = 'data.json'
    output_file = 'processed_data.json'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    processed_data = process_data(data)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)
    print("Data processed and saved successfully.")

if __name__ == "__main__":
    main()
