# GetWeather.py
# Get Weather class. Get weather infomation from OpenWeather API
# By Monster Kid

import requests

class GetWeather(object):
    """
    GetWeather class to get weather infomation
    Methods:
        :get_current_weather: get current weather infomation of the city
        :get_forecast_weather: get forecast weather infomation of the city
    """

    # OpenWeather API URL
    CURRENT_URL = 'http://api.openweathermap.org/data/2.5/weather?'
    FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast?'
    # OpenWeather developer key
    KEY = '5054a579440524d0c6cd3a2ea339d3a7'

    def __init__(self):

        # API url and developer key
        self.current_url = self.CURRENT_URL + 'appid=' + self.KEY
        self.forecast_url = self.FORECAST_URL + 'appid=' + self.KEY

    def get_current_weather(self, city_name: str) -> tuple:
        """
        Get current weather infomation of the city
        Parameters:
            :param city_name: name of the city(str)
        Return:
            :return: weather infomation(tuple) 
            please refer to format_current_weather to get the
            format of the returned tuple
        """

        # create request url
        url = self.current_url + '&q=' + city_name
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()
        data = self.format_current_weather(data)
        # check if the request is successful
        if data[0] != 200:
            return None
        return data 

    def get_forecast_weather(self, city_name: str) -> tuple:
        """
        Get forecast weather infomation of the city
        Parameters:
            :param city_name: name of the city(str)
        Return:
            :return: weather infomation(tuple) 
            please refer to format_forecast_weather to get the
            format of the returned tuple
        """

        # create request url
        url = self.forecast_url + '&q=' + city_name
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()
        data = self.format_forecast_weather(data)
        # check if the request is successful
        if data[0] != 200:
            return None
        return data
    
    def format_current_weather(self, data: dict) -> tuple:
        """
        Format current weather infomation
        Parameters:
            :param data: weather infomation(dict)
        Return:
            :return: formatted weather infomation(tuple) 
            - the first element is the get status:
                - 200: successful
                - 404: city not found
                - 401: invalid API key
            - the second element is the city information:
                - city name('name')
                - country('country')
                - timezone('timezone')
                - latitude and longitude(in 'coord' dict: 'lat', 'lon')
                - sunrise and sunset(in 'sun' dict: 'sunrise', 'sunset')
            - the third element is the weather information:
                - weather dict('weather')
                    - weather('main')
                    - weather description('description')
                    - weather icon('icon')
                - temperature dict('main')
                    - temperature('temp')
                    - feels like('feels_like')
                    - minimum temperature('temp_min')
                    - maximum temperature('temp_max')
                    - pressure('pressure')
                    - sea level pressure('sea_level')
                    - ground level pressure('grnd_level')
                    - humidity('humidity')
                - visibility('visibility')
                - wind dict('wind')
                    - wind speed('speed')
                    - wind direction('deg')
                    - wind gust('gust')
                - cloudiness('clouds')
        """
        
        # I'm currently using Openweather API
        result = [None, None, None]
        # the first element is the get status
        result[0] = int(data['cod'])
        # the second element is the city information
        result[1] = {}
        result[1]['name'] = data['name']
        result[1]['country'] = data['sys']['country']
        result[1]['timezone'] = data['timezone']
        result[1]['coord'] = data['coord']
        result[1]['sun'] = {}
        result[1]['sun']['sunrise'] = data['sys']['sunrise']
        result[1]['sun']['sunset'] = data['sys']['sunset']
        # the third element is the weather information
        result[2] = {}
        result[2]['weather'] = data['weather'][0]
        result[2]['main'] = data['main']
        result[2]['visibility'] = data['visibility']
        result[2]['wind'] = data['wind']
        result[2]['clouds'] = data['clouds']['all']

        return tuple(result)

    def format_forecast_weather(self, data: list) -> tuple:
        """
        Format forecast weather infomation
        Parameters:
            :param data: weather infomation(list)
        Return:
            :return: formatted weather infomation(tuple) 
            - the first element is the get status:
                please refer to format_current_weather
            - the second element is the city information:
                please refer to format_current_weather
            - the third element is the weather information:
                the weather information is a list of weather information, 
                each element is a dict: refer to format_current_weather
                and the dict has an additional key 'time'
                - time: dict of time information
                    - time stamp('dt')
                    - time string('dt_txt'): format: 'YYYY-MM-DD HH:MM:SS'
        """

        # I'm currently using Openweather API
        result = [None, None, None]
        # the first element is the get status
        result[0] = int(data['cod'])
        # the second element is the city information
        result[1] = {}
        result[1]['name'] = data['city']['name']
        result[1]['country'] = data['city']['country']
        result[1]['timezone'] = data['city']['timezone']
        result[1]['coord'] = data['city']['coord']
        result[1]['sun'] = {}
        result[1]['sun']['sunrise'] = data['city']['sunrise']
        result[1]['sun']['sunset'] = data['city']['sunset']
        # the third element is the weather information
        result[2] = []
        for item in data['list']:
            result[2].append({})
            result[2][-1]['weather'] = item['weather'][0]
            result[2][-1]['main'] = item['main']
            result[2][-1]['visibility'] = item['visibility']
            result[2][-1]['wind'] = item['wind']
            result[2][-1]['clouds'] = item['clouds']['all']
            result[2][-1]['time'] = {}
            result[2][-1]['time']['dt'] = item['dt']
            result[2][-1]['time']['dt_txt'] = item['dt_txt']

        return tuple(result)

    
if __name__ == '__main__':
    gw = GetWeather()
    data1 = gw.get_current_weather('Sydney')
    data2 = gw.get_forecast_weather('Sydney')
    print(data1)
    print(data2)
