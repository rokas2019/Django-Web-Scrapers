import requests
from bs4 import BeautifulSoup


def get_page_links(link, num_pages):
    list_page_links = [link]

    for i in range(1, num_pages):
        list_page_links.append(f'{link}?p={i + 1}')

    return list_page_links


def sort_stories_by_votes(hn_list):
    return sorted(hn_list, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(list_links, list_subtext):
    hn_list = []
    for i, item in enumerate(list_links):
        title = item.getText()
        href = item.get('href', None)
        vote = list_subtext[i].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100:
                hn_list.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn_list)


def create_mega_link_list(pages_links):
    links = []
    subtext = []
    mega_link_list = []

    for link in pages_links:
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        links += soup.select('.titlelink')  # . means that it's a class
        subtext += soup.select('.subtext')

    mega_link_list.append(create_custom_hn(links, subtext))

    return mega_link_list
