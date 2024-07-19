import requests
from geopy.geocoders import Nominatim


class CityNotFoundError(Exception):
    pass


def get_coordinates(city_name):
    geolocator = Nominatim(user_agent='weather_app')
    location = geolocator.geocode(city_name)
    if location is None:
        raise CityNotFoundError(f'Город «{city_name}» не найден.')
    return {'latitude': location.latitude, 'longitude': location.longitude}


def get_weather(city):
    try:
        coordinates = get_coordinates(city)
    except CityNotFoundError as e:
        return None, str(e)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coordinates['latitude']}&longitude={coordinates['longitude']}&hourly=temperature_2m"
    response = requests.get(url)
    return response.json(), None
