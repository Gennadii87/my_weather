import json

from django.shortcuts import render
from django.http import JsonResponse
from .api import get_weather
from .models import CitySearch
from django.views.decorators.http import require_GET
from django.db.models import Sum


def weather_view(request):
    if request.method == 'POST':
        city = request.POST.get('city')

        if not city:
            return render(request, 'weather/weather.html',
                          {'error_message': 'Введите название города'})

        weather_data = get_weather(city)
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        city_search, created = CitySearch.objects.get_or_create(
            session_key=session_key,
            city_name=city
        )
        if not created:
            city_search.search_count += 1
            city_search.save()

        request.session['last_city'] = city

        history_response = search_history(request)
        history_data = json.loads(history_response.content)

        return render(request, 'weather/weather.html',
                      {
                                'weather_data': weather_data,
                                'city': city,
                                'history': history_data.get('history')
                            })

    last_city = request.session.get('last_city')
    return render(request, 'weather/weather.html', {'last_city': last_city})


def search_history(request):
    session_key = request.session.session_key
    city_searches = CitySearch.objects.filter(session_key=session_key)
    return JsonResponse({'history': list(city_searches.values())})


def last_search(request):
    last_city = request.session.get('last_city')
    return JsonResponse({'last_city': last_city})


@require_GET
def autocompletion(request):
    query = request.GET.get('q', '')
    if len(query) > 1:
        cities = CitySearch.objects.filter(city_name__icontains=query).values_list('city_name', flat=True)
        autocomplete = list(cities)
    else:
        autocomplete = []

    return JsonResponse({'autocomplete': autocomplete})


@require_GET
def city_request_count(request):
    city_name = request.GET.get('city')
    city_search = CitySearch.objects.filter(city_name=city_name).first()
    count = city_search.search_count if city_search else 0
    return JsonResponse({'count': count})


@require_GET
def all_city_request_counts(request):
    city_searches = CitySearch.objects.all()
    counts = city_searches.values('city_name').annotate(search_count=Sum('search_count'))
    return JsonResponse({'counts': list(counts)})
