from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

# I'm not a bot haha
header = {'User-Agent': 'Mozilla/5.0'}


def adjust_url(key_word) -> str:
    url = f'https://www.reddit.com/domain/old.reddit.com/search/?q={str(key_word)}&sort=relevance&t=day'
    return url


def get_reddit_text(url) -> list[str]:
    texts = requests.get(url, headers=header).text
    return texts


def parse_required_fields(text) -> list[dict]:
    result = []
    text_to_str = str(text)
    soup = BeautifulSoup(text_to_str, 'lxml')
    articles = soup.find_all('header', class_='search-result-header')[3:6]
    for index, article in enumerate(articles, 1):
        article_items = {
            'index': index,
            'title': article.find('a', class_='search-title may-blank').text.replace('\\n', ''),
            'link': article.find('a', class_='search-title may-blank').attrs['href']
        }
        result.append(article_items)
    return result


def write_to_sql() -> None:
    conn = sqlite3.connect('reddit_db')
    c = conn.cursor()
    conn.commit()
    articles = parse_required_fields(get_reddit_text())
    df = pd.DataFrame(articles, columns=['index', 'title', 'link'])
    df.to_sql('articles', conn, if_exists='replace', index=False)
    c.execute('''
    SELECT * FROM articles
    ''')



