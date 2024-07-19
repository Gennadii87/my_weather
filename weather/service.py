import os
import requests
from cache_memoize import cache_memoize

import plotly.graph_objects as go
from plotly.io import to_html
import pandas as pd

from geopy.geocoders import Nominatim
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import CitySearch


class CityNotFoundError(Exception):
    pass


def get_coordinates(city_name):
    geolocator = Nominatim(user_agent='weather_app')
    location = geolocator.geocode(city_name)
    if location is None:
        raise CityNotFoundError(f'Город «{city_name}» не найден.')
    return {'latitude': location.latitude, 'longitude': location.longitude}


@cache_memoize(30)
def get_weather(city):
    try:
        coordinates = get_coordinates(city)
    except CityNotFoundError as e:
        return None, str(e)
    url = f"https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": f"{coordinates['latitude']}",
        "longitude": f"{coordinates['longitude']}",
        "timezone": "GMT",
        "hourly": "temperature_2m",
        "past_days": 0,
        "forecast_days": 3
    }
    response = requests.get(url, params=params)
    return response.json(), None


@require_GET
def autocompletion(request):
    query = request.GET.get('q', '')

    if len(query) > 1:
        cities = CitySearch.objects.filter(city_name__icontains=query).values_list('city_name', flat=True)
        autocomplete = list(cities)

        if not autocomplete:

            file_path = os.path.join(os.path.dirname(__file__), 'cities.txt')
            with open(file_path, 'r', encoding='utf-8') as file:
                all_cities = file.readlines()
                autocomplete = [city.strip() for city in all_cities if query.lower() in city.lower()]

    return JsonResponse({'autocomplete': autocomplete})


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
