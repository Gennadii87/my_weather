import requests
from geopy.geocoders import Nominatim


def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city_name)
    return {'latitude': location.latitude, 'longitude': location.longitude}


def get_weather(city):
    coordinates = get_coordinates(city)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coordinates['latitude']}&longitude={coordinates['longitude']}&hourly=temperature_2m"
    response = requests.get(url)
    return response.json()
