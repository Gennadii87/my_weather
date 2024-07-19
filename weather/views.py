import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .service import get_weather
from .models import CitySearch
from django.views.decorators.http import require_GET
from django.db.models import Sum

import plotly.graph_objects as go
import pandas as pd
from plotly.io import to_html
from datetime import datetime


@csrf_exempt
def weather_view(request):
    if request.method == 'POST':
        city = request.POST.get('city')

        if not city:
            return render(request, 'weather/weather.html',
                          {'error_message': 'Введите название города'})

        weather_data, error_message = get_weather(city)

        if error_message:
            return render(request, 'weather/weather.html', {'error_message': error_message})

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

        temperature_graph, now, closest_temperature = create_interactive_temperature_plot(weather_data)

        return render(request, 'weather/weather.html',
                      {
                                'weather_data': weather_data,
                                'city': city,
                                'history': history_data.get('history'),
                                'temperature_graph': temperature_graph,
                                'now': now,
                                'closest_temperature': closest_temperature
                            })

    last_city = request.session.get('last_city')
    return render(request, 'weather/weather.html', {'last_city': last_city})


def create_interactive_temperature_plot(weather_data):

    df = pd.DataFrame({
        'time': pd.to_datetime(weather_data['hourly']['time']),
        'temperature': weather_data['hourly']['temperature_2m']
    })

    now = pd.to_datetime('now')

    # Находим ближайшее время и соответствующую температуру
    closest_time_index = df['time'].sub(now).abs().idxmin()
    closest_temperature = df['temperature'].iloc[closest_time_index]

    fig = go.Figure()
    fig.add_vline(x=now, line=dict(color="black", width=2, dash="dash"))
    fig.add_trace(go.Scatter(x=df['time'], y=df['temperature'], mode='lines+markers', name='Температура'))
    fig.add_annotation(
        x=now,
        y=max(df['temperature']),
        text="Текущее время",
        showarrow=True,
        arrowhead=5,
        ax=-60,
        ay=-40,
        font=dict(color="red")
    )
    fig.update_layout(title='Температура от времени', xaxis_title='Время', yaxis_title='Температура (°C)')

    temperature_graph = to_html(fig, full_html=False)

    return temperature_graph, now, closest_temperature


def search_history(request):
    session_key = request.session.session_key
    city_searches = CitySearch.objects.filter(session_key=session_key)
    return JsonResponse({'history': list(city_searches.values())})


def last_search(request):
    last_city = request.session.get('last_city')
    return JsonResponse({'last_city': last_city})


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
