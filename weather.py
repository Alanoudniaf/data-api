# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com"

def search_city(query):
    '''
    Look for a given city. If multiple options are returned, have the user choose between them.
    Return one city (or None)
    '''
    url = urllib.parse.urljoin(BASE_URI, "/geo/1.0/direct")
    response = requests.get(url, params={'q': query, 'limit': 5})
    cities = response.json()

    if not cities:
        print(f"Sorry, OpenWeather does not know about {query}!")
        return None

    if len(cities) == 1:
        return cities[0]

    for idx, city in enumerate(cities, start=1):
        print(f"{idx}. {city['name']}, {city['country']}")

    try:
        index = int(input("Multiple matches found, which city did you mean?\n> ")) - 1
        return cities[index] if 0 <= index < len(cities) else None
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None

def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    url = urllib.parse.urljoin(BASE_URI, "/data/2.5/forecast")
    response = requests.get(url, params={'lat': lat, 'lon': lon, 'units': 'metric'})
    forecasts = response.json().get('list', [])

    return forecasts[::8] if forecasts else []

def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)

    if city:
        daily_forecasts = weather_forecast(city['lat'], city['lon'])

        for forecast in daily_forecasts:
            max_temp = round(forecast['main']['temp_max'])
            weather_desc = forecast['weather'][0]['main']
            date = forecast['dt_txt'].split()[0]
            print(f"{date}: {weather_desc} ({max_temp}°C)")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
