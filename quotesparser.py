import requests
from bs4 import BeautifulSoup
import json


# Функция для сбора цитат и авторов с одной страницы
def scrape_quotes(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = []

    for quote in soup.find_all(class_='quote'):
        text = quote.find(class_='text').get_text()
        author = quote.find(class_='author').get_text()

        # Опционально можем добавить теги, если они есть
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]

        quotes.append({
            'text': text,
            'author': author,
            'tags': tags
        })

    return quotes


# Собираем все цитаты со всех страниц
base_url = 'https://quotes.toscrape.com'
all_quotes = []
page_num = 1

while True:
    page_url = f'{base_url}/page/{page_num}/'
    print(f'Собираю данные с {page_url}')

    quotes = scrape_quotes(page_url)

    if not quotes:
        break

    all_quotes.extend(quotes)
    page_num += 1

# Сохраняем результат в JSON файл
with open('quotes.json', 'w') as file:
    json.dump(all_quotes, file, indent=4)

print("Сбор данных завершен! Результаты сохранены в файле 'quotes.json'.")