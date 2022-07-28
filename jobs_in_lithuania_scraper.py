import numpy as np
from bs4 import BeautifulSoup
import requests

pages = np.arange(1, 3, 1)
# I'm not a bot haha
header = {'User-Agent': 'Mozilla/5.0'}


def get_data(key_word) -> list[str]:
    texts = []
    url = f'https://www.cvbankas.lt/?keyw={key_word}&page='
    for page in pages:
        page = url + str(page)
        text = requests.get(page).text
        texts.append(text)
    return texts


def parse_required_fields(texts) -> list[dict]:
    result = []
    texts = str(texts)
    soup = BeautifulSoup(texts, 'lxml')
    jobs = soup.find_all('article', class_='list_article list_article_rememberable jobadlist_list_article_rememberable')
    for index, job in enumerate(jobs, 1):
        job_item = {
            'index': index,
            'title': job.find('h3', class_='list_h3').text.replace('\\n', '').replace(' ', ''),
            'company_name': job.find('span', class_='dib mt5').text.replace('\\n', '').replace(' ', ''),
            'city_or_country': job.find('span', class_='list_city').text.replace('\\n', '').replace(' ', ''),
            'advertisement_link': job.find('a', class_='list_a can_visited list_a_has_logo') \
                .attrs['href'].replace('\\n', '')}
        try:
            job_item['salary'] = job.find('span', class_='salary_amount').text.replace('\\n', '').replace(' ', '')
        except AttributeError:
            job_item['salary'] = 'not specified'

        result.append(job_item)

    return result


