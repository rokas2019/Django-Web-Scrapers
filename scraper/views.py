from django.shortcuts import render
from reddit_scraper import get_reddit_text, adjust_url, parse_required_fields
from hackaday_scraper import get_hackaday_text, adjust_hackaday_url, parse_hd_required_fields


def keyword(request) -> str:
    key_word = request.GET.get('topic')
    key_word = key_word.replace(' ', '+')
    return key_word


def scraper_home(request):
    reddit_result = None
    hackaday_result = None
    if "topic" in request.GET:
        reddit_result = parse_required_fields(get_reddit_text(adjust_url(keyword(request))))
        hackaday_result = parse_hd_required_fields(get_hackaday_text(adjust_hackaday_url(keyword(request))))
    return render(request, 'scraper/scraper_home.html', {'reddit_result': reddit_result, 'hackaday_result': hackaday_result})
