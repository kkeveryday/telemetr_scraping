import requests
from bs4 import BeautifulSoup
import os

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                     'application/signed-exchange;v=b3;q=0.9'}
FILE = 'telemetr.txt'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='btn')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id='channels_table')

    links = []
    for tr in table.find_all('tr'):
        for td in tr.find_all('td', class_='wd-300 pb-0 overflow-hidden'):
            links.append({
                'Title': td.find('a').get_text(strip=True),
                'Link': td.find('a').get('href')
            })
    return links


def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf8') as file:
        for item in items:
            for key, value in item.items():
                file.write('{}:{}\n'.format(key, value))
            file.write('\n')


def parse():
    channel = input('Введите категорию: ')
    channel = channel.strip()
    URL = f'https://telemetr.me/channels/cat/{channel}/'
    html = get_html(URL)
    if html.status_code == 200:
        links = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            links.extend(get_content(html.text))
        save_file(links, FILE)
        print(f'Получено {len(links)} ссылок')
        os.startfile(FILE)
    else:
        print('Error')


parse()
