import requests
from bs4 import BeautifulSoup
import json
import os

def get_text_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_div = soup.find('div', id='text')
        if text_div:
            text = '\n'.join([element.get_text(strip=True) for element in text_div.find_all(['p', 'h1', 'h2', 'h3', 'z', 'o'])])
            return text
        return None
    except Exception as e:
        print(f"Ошибка при получении текста с {url}: {e}")
        return None

def get_all_text(start_url, end_url, start_page, end_page):
    all_text = []
    for page_number in range(start_page, end_page + 1):
        current_url = f"{start_url}{page_number}{end_url}"
        text = get_text_from_page(current_url)
        if text:
            all_text.append(text)
            print(f"Обработано: {current_url}")
    
    return '\n'.join(all_text)

def save_as_json(data, filename):
    existing_data = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = []
        except json.JSONDecodeError as e:
            print(f"Ошибка при чтении существующего JSON файла: {e}")
    
    existing_data.append(data)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
        print("Данные успешно сохранены в формате JSON.")
    except Exception as e:
        print(f"Ошибка при сохранении данных в JSON файл: {e}")

def main():
    start_url = 'https://ilibrary.ru/text/26/p.'  # Замените на нужный URL
    end_url = '/index.html'
    start_page = 1
    end_page = 1
    output_file = 'data.json'

    # Получение полного текста произведения
    text = get_all_text(start_url, end_url, start_page, end_page)

    # Формирование данных для сохранения
    data = {
        'title': 'Чужая жена и муж под кроватью',
        'text': text
    }

    # Сохранение данных в JSON файл
    save_as_json(data, output_file)

if __name__ == "__main__":
    main()
