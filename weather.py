import requests
from bs4 import BeautifulSoup
import geocoder
import json

# Declaration of global variables
degree_sign = u"\N{DEGREE SIGN}"

# Given a lattitude and longtitude, this function will return
# the closest city that is with the 'metaweather' api database
def getClosestCityIdByLocation(latt, long):
    api_link = 'https://www.metaweather.com/api/location/search/?lattlong={:.2f},{:.2f}'.format(latt, long)
    res = requests.get(api_link)
    res_text = res.text
    data = json.loads(res_text)
    closest_city_id = data[0]['woeid']
    return closest_city_id

# Returns the weather data of the city given the corresponding
# 'woeid'
# The 'woeid' is an identifier used by the 'metaweather' api
# to identify a city
def getWeatherDataByID(id):
    api_link = 'https://www.metaweather.com/api/location/{:d}'.format(id)
    res = requests.get(api_link)
    res_text = res.text
    data = json.loads(res_text)
    return data

# Display the current data when passed in a dictionary object that contain
# the 'min_temp', 'max_temp', 'the_temp' (cur_temp), 'wind_speed',
# 'wind_direction', and 'humidity'
def displayData(data):
    print('Min Temp: {:2.02f}{:s}C'.format(data['min_temp'], degree_sign))
    print('Max Temp: {:2.02f}{:s}C'.format(data['max_temp'], degree_sign))
    print('Cur Temp: {:2.02f}{:s}C'.format(data['the_temp'], degree_sign))
    print('Wind Speed: {:2.02f}mph'.format(data['wind_speed']))
    print('Wind Direction: {:2.02f}{:s}'.format(data['wind_direction'], degree_sign))
    print('Humidity: {:2.02f}%'.format(data['humidity']))

# Gets the location of the current user based on the users
# IP address
# Uses the users IP address to get their current lotitude
# and longtitude using the geocoder library
def getCurrentLatLong():
    g = geocoder.ip('me')
    return g.latlng

def main():
    cur_location = getCurrentLatLong()
    closest_city_ID = getClosestCityIdByLocation(cur_location[0], cur_location[1])
    data = getWeatherDataByID(closest_city_ID)
    weather_data = data['consolidated_weather']
    weather_data_today = weather_data[0]
    weather_data_tomorrow = weather_data[1]
    print('## Today Weather Data in {:s} ##'.format(data['title']))
    displayData(weather_data_today)
    print('\n## Tomorrow Weather Data in {:s} ##'.format(data['title']))
    displayData(weather_data_tomorrow)

# Main Functoin
if __name__ == '__main__':
    main()
