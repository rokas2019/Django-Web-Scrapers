from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

# I'm not a bot haha
header = {'User-Agent': 'Mozilla/5.0'}


def adjust_hackaday_url(key_word) -> str:
    url = f'https://hackaday.com/blog/?s={str(key_word)}'
    return url


def get_hackaday_text(url) -> list[str]:
    texts = requests.get(url, headers=header).text
    return texts


def parse_hd_required_fields(text) -> list[dict]:
    result = []
    text_to_str = str(text)
    soup = BeautifulSoup(text_to_str, 'html.parser')
    articles = soup.find_all('h1', class_='entry-title')[:3]
    for index, article in enumerate(articles, 1):
        article_items = {
            'index': index,
            'title': article.find('a', class_=False, id=False).text.replace('\\n', ''),
            'link': article.find('a', class_=False, id=False).attrs['href']
        }
        result.append(article_items)
    return result


def write_to_sql() -> None:
    conn = sqlite3.connect('reddit_db')
    c = conn.cursor()
    conn.commit()
    articles = parse_hd_required_fields(get_hackaday_text())
    df = pd.DataFrame(articles, columns=['index', 'title', 'link'])
    df.to_sql('articles', conn, if_exists='replace', index=False)
    c.execute('''
    SELECT * FROM articles
    ''')


