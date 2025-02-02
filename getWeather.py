# GetWeather.py
# Get Weather class. Get weather infomation from OpenWeather API
# By Monster Kid

import requests

class GetWeather(object):
    """
    GetWeather class to get weather infomation
    Methods:
        - get_ow_current: get current weather infomation from OpenWeather API
        - get_ow_forecast: get forecast weather infomation from OpenWeather API
        - get_hf_location: get location information from HeFeng API
        - get_hf_current: get current weather infomation from HeFeng API
        - get_hf_7days: get 7 days weather infomation from HeFeng API
        - get_hf_24hours: get 24 hours weather infomation from HeFeng API
        - get_hf_rain: get rain infomation from HeFeng API
        - get_hf_warning: get warning infomation from HeFeng API
        - get_hf_indices: get indices infomation from HeFeng API
        - get_hf_air: get air infomation from HeFeng API
        - get_hf_air_forecast: get air forecast infomation from HeFeng API
    """

    # OpenWeather API URL
    OW_URL_CURRENT = 'http://api.openweathermap.org/data/2.5/weather?'
    OW_URL_FORECAST = 'http://api.openweathermap.org/data/2.5/forecast?'
    # OpenWeather developer key
    OW_KEY = '5054a579440524d0c6cd3a2ea339d3a7'
    # HeFeng API URL
    HF_URL_LOCATION = 'https://geoapi.qweather.com/v2/city/lookup?'
    HF_URL_CURRENT = 'https://devapi.qweather.com/v7/weather/now?'
    HF_URL_7DAYS = 'https://devapi.qweather.com/v7/weather/7d?'
    HF_URL_24HOURS = 'https://devapi.qweather.com/v7/weather/24h?'
    HF_URL_RAIN = 'https://devapi.qweather.com/v7/minutely/5m?'
    HF_URL_WARNING = 'https://devapi.qweather.com/v7/warning/now?'
    HF_URL_INDICES = 'https://devapi.qweather.com/v7/indices/3d?'
    HF_URL_AIR = 'https://devapi.qweather.com/v7/air/now?'
    HF_URL_AIR_FORECAST = 'https://devapi.qweather.com/v7/air/5d?'
    # HeFeng developer key
    HF_KEY = '55c7da0804024e868a70beb00fcd8c03'

    def __init__(self, language: str = 'en'):
        """
        Init GetWeather class
        Parameters:
            :param language: language(str)
        """

        # OpenWeather API URL(deprecated)
        self.ow_url_current = self.OW_URL_CURRENT + 'appid=' + self.OW_KEY
        self.ow_url_forecast = self.OW_URL_FORECAST + 'appid=' + self.OW_KEY

        # Concatenate URL with developer key(actually redundant, because set_hf_language will concatenate URL again)
        self.hf_language = language
        self.hf_url_location = self.HF_URL_LOCATION + 'key=' + self.HF_KEY
        self.hf_url_current = self.HF_URL_CURRENT + 'key=' + self.HF_KEY
        self.hf_url_7days = self.HF_URL_7DAYS + 'key=' + self.HF_KEY
        self.hf_url_24hours = self.HF_URL_24HOURS + 'key=' + self.HF_KEY
        self.hf_url_rain = self.HF_URL_RAIN + 'key=' + self.HF_KEY
        self.hf_url_warning = self.HF_URL_WARNING + 'key=' + self.HF_KEY
        self.hf_url_indices = self.HF_URL_INDICES + 'key=' + self.HF_KEY
        self.hf_url_air = self.HF_URL_AIR + 'key=' + self.HF_KEY
        self.hf_url_air_forecast = self.HF_URL_AIR_FORECAST + 'key=' + self.HF_KEY
        # set language
        self.set_hf_language(language)
    
    ## --- Set language --- ##

    def set_hf_language(self, language: str):
        """
        Set language of HeFeng API, change URL accordingly
        Parameters:
            :param language: language(str)
        """
        # check language
        if language not in ['zh', 'en']:
            raise ValueError('Language must be "zh" or "en"')
        # set language
        self.hf_language = language
        # concatenate URL with language
        self.hf_url_current = self.HF_URL_CURRENT + 'key=' + self.HF_KEY + '&lang=' + self.hf_language
        self.hf_url_7days = self.HF_URL_7DAYS + 'key=' + self.HF_KEY + '&lang=' + self.hf_language
        self.hf_url_24hours = self.HF_URL_24HOURS + 'key=' + self.HF_KEY + '&lang=' + self.hf_language
        self.hf_url_rain = self.HF_URL_RAIN + 'key=' + self.HF_KEY + '&lang=' + self.hf_language
        self.hf_url_warning = self.HF_URL_WARNING + 'key=' + self.HF_KEY + '&lang=' + self.hf_language
        self.hf_url_indices = self.HF_URL_INDICES + 'key=' + self.HF_KEY + '&lang=' + self.hf_language
        self.hf_url_air = self.HF_URL_AIR + 'key=' + self.HF_KEY + '&lang=' + self.hf_language
        self.hf_url_air_forecast = self.HF_URL_AIR_FORECAST + 'key=' + self.HF_KEY + '&lang=' + self.hf_language

    ## --- GET request --- ##

    ## OpenWeather API ##

    def get_ow_current(self, city_name: str) -> dict:
        """
        Get current weather infomation of the city
        Parameters:
            :param city_name: name of the city(str)
        Return:
            :return: weather infomation(dict)
            please refer to OpenWeather API document
        """

        # create request url
        url = self.ow_url_current + '&q=' + city_name
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()

        return data 

    def get_ow_forecast(self, city_name: str) -> dict:
        """
        Get forecast weather infomation of the city
        Parameters:
            :param city_name: name of the city(str)
        Return:
            :return: weather infomation(dict)
            please refer to OpenWeather API document
        """

        # create request url
        url = self.ow_url_forecast + '&q=' + city_name
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()

        return data

    ## HeFeng API ##

    def get_hf_location(self, location: str) -> str:
        """
        Get location information of the city
        Parameters:
            :param location: name of the city(str)
        Return:
            :return: id of the city(str)
        """

        # create request url
        url = self.hf_url_location + '&location=' + location
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()
        # check if the request is successful, if not return None
        if data['code'] != '200':
            return None

        # response is a list of location sorted by priority, return the first one
        return data["location"][0]

    def get_hf_current(self, id: str) -> dict:
        """
        Get current weather infomation of the city
        Parameters:
            :param location: name of the city(str)
        Return:
            :return: weather infomation(dict) 
            - code
            - updateTime
            - now: obsTime, temp, feelsLike, icon, text, wind360, windDir, windScale, windSpeed, humidity, precip, pressure, vis, cloud, dew
            - refer: sources, license
        """

        # create request url
        url = self.hf_url_current + '&location=' + id
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()

        return data

    def get_hf_7days(self, id: str) -> dict:
        """
        Get 7 days weather infomation of the city
        Parameters:
            :param location: name of the city(str)
        Return:
            :return: weather infomation(dict) 
            - code
            - updateTime
            - daily: fxDate, sunrise, sunset, moonrise, moonset, moonPhase, tempMax, tempMin, iconDay, textDay, iconNight, textNight, wind360Day, windDirDay, windScaleDay, windSpeedDay, wind360Night, windDirNight, windScaleNight, windSpeedNight, humidity, precip, pressure, vis, cloud, uvIndex
            - refer: sources, license
        """

        # create request url
        url = self.hf_url_7days + '&location=' + id
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()

        return data
    
    def get_hf_24hours(self, id: str) -> dict:
        """
        Get 24 hours weather infomation of the city
        Parameters:
            :param location: name of the city(str)
        Return:
            :return: weather infomation(dict) 
            - code
            - updateTime
            - hourly: fxTime, temp, icon, text, wind360, windDir, windScale, windSpeed, windScale, windSpeed, humidity, precip, pressure, cloud, dew
            - refer: sources, license
        """

        # create request url
        url = self.hf_url_24hours + '&location=' + id
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()

        return data

    def get_hf_rain(self, lat: str, lon: str) -> dict:
        """
        Get rain infomation of the city
        Parameters:
            :param location: name of the city(str)
        Return:
            :return: weather infomation(dict) 
            - code
            - updateTime
            - summary: fxDate, fxTime, precip
            - refer: sources, license
        """

        # create request url
        # round to 2 decimal places after the decimal point
        # NOTE: both lat and lon are string
        lat = str(round(float(lat), 2))
        lon = str(round(float(lon), 2))
        url = self.hf_url_rain + '&location=' + lon + ',' + lat
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()

        return data

    def get_hf_warning(self, id: str) -> dict:
        """
        Get warning infomation of the city
        Parameters:
            :param location: name of the city(str)
        Return:
            :return: weather infomation(dict) 
            - code
            - updateTime
            - warning: id, sender, pubTime, title, startTime, endTime, status, level, type, typeName, text, related, relatedName
            - refer: sources, license
        """

        # create request url
        url = self.hf_url_warning + '&location=' + id
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()

        return data

    def get_hf_indices(self, id: str) -> dict:
        """
        Get indices infomation of the city
        Parameters:
            :param location: name of the city(str)
        Return:
            :return: weather infomation(dict) 
            - code
            - updateTime
            - daily: fxDate, sunrise, sunset, moonrise, moonset, moonPhase, tempMax, tempMin, iconDay, textDay, iconNight, textNight, wind360Day, windDirDay, windScaleDay, windSpeedDay, wind360Night, windDirNight, windScaleNight, windSpeedNight, humidity, precip, pressure, vis, cloud, uvIndex
            - refer: sources, license
        """

        # create request url
        url = self.hf_url_indices + '&location=' + id + "&type=0"
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()

        return data

    def get_hf_air(self, id: str) -> dict:
        """
        Get air infomation of the city
        Parameters:
            :param location: name of the city(str)
        Return:
            :return: weather infomation(dict) 
            - code
            - updateTime
            - now: pubTime, aqi, level, category, primary, pm10, pm2p5, no2, so2, co, o3, description
            - refer: sources, license
        """

        # create request url
        url = self.hf_url_air + '&location=' + id
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()

        return data

    def get_hf_air_forecast(self, id: str) -> dict:
        """
        Get air forecast infomation of the city
        Parameters:
            :param location: name of the city(str)
        Return:
            :return: weather infomation(dict) 
            - code
            - updateTime
            - daily: fxDate, aqi, level, category, primary, pm10, pm2p5, no2, so2, co, o3, description
            - refer: sources, license
        """

        # create request url
        url = self.hf_url_air_forecast + '&location=' + id
        # GET request
        response = requests.get(url)
        # decode the response
        data = response.json()

        return data

    
## --- Test --- ##

if __name__ == '__main__':
    gw = GetWeather()
    data1 = gw.get_ow_current('Sydney')
    data2 = gw.get_ow_forecast('Sydney')
    print(data1)
    print(data2)
    print('----------------------------------------')
    print()
    city = 'Beijing'
    id = gw.get_hf_location(city)
    data_current = gw.get_hf_current(city)
    data_7days = gw.get_hf_7days(city)
    data_24hours = gw.get_hf_24hours(city)
    data_rain = gw.get_hf_rain(city)
    data_warning = gw.get_hf_warning(city)
    data_indices = gw.get_hf_indices(city)
    data_air = gw.get_hf_air(city)
    data_air_forecast = gw.get_hf_air_forecast(city)
    print(id)
    print('###')
    print(data_current)
    print('###')
    print(data_7days)
    print('###')
    print(data_24hours)
    print('###')
    print(data_rain)
    print('###')
    print(data_warning)
    print('###')
    print(data_indices)
    print('###')
    print(data_air)
    print('###')
    print(data_air_forecast)
    print('----------------------------------------')
    print()

