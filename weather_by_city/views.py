from django.shortcuts import render
from weather_scraper import get_all_data


def get_ip(request) -> str:
    ip = request.GET.get('ip')
    return ip


def weather_by_city(request):
    weather_result = None
    if 'ip' in request.GET:
        weather_result = get_all_data(get_ip(request))
        print(f'results{weather_result}')
    return render(request, 'weather_by_city/weather_by_city.html', {'result': weather_result})
