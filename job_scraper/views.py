from django.shortcuts import render
from jobs_in_lithuania_scraper import get_data, parse_required_fields


def get_keyword(request) -> str:
    key_word = request.GET.get('key_word')
    return key_word


def job_scraper(request):
    job_result = None
    if 'key_word' in request.GET:
        job_result = parse_required_fields(get_data(get_keyword(request)))
    return render(request, 'job_scraper/job_scraper.html', {'result': job_result})
