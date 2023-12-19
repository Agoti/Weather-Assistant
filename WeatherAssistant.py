# WeatherAssistant.py
# Description: Weather Assistant class to manage weather infomation
#     This is the controller of the program
# By Monster Kid
from GetWeather import *
import concurrent.futures

class WeatherAssistant(object):
    """
    WeatherAssistant class to manage weather infomation
    Methods:
        - add_city: add a city to city list
        - remove_city: remove a city from city list
        - shift_city: shift current city
        - update_weather: update current and forecast weather
    """

    # the file to store city list
    CITIES_FILE = 'data/cities.txt' 
    ALL_CITY = 'data/all_city.csv'
    EMPTY_WEATHER_DICT = {'now' : None, '7d' : None, '24h' : None, 'rain' : None, 'warning' : None, 'indices' : None,
                      'air' : None, 'air_forecast' : None}

    def __init__(self, language='en', do_not_update=False):
        self.get_weather = GetWeather(language)
        self.language = language
        self.cities, self.current_city = self.load_cities()
        self.all_city_list = self.load_all_city()
        self.language = 'en'
        self.weather = self.EMPTY_WEATHER_DICT
        if not do_not_update:
            self.update_weather()

    def set_language(self, language: str):
        """
        Set language
        """
        try:
            self.language = language
            self.get_weather.set_language(language)
            self.update_weather()
            return "Success"
        except ValueError as e:
            return str(e)
        except:
            return "Unknown error"

    
    def load_cities(self) -> tuple:
        """
        Load cities from city file
        """
        try:
            cities = []
            current_city = None
            with open(WeatherAssistant.CITIES_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    city = line.strip()
                    cities.append(city)
                    if current_city is None:
                        current_city = city
            return cities, current_city
        except:
            return [], None

    def load_all_city(self) -> list:
        """
        Load all city list from csv file
        all_city_list: list of 3-tuple: (EnglishName, CNInfo_dict, ENInfo_dict)
        - EnglishName: English name of the city
        - CNInfo_dict: Chinese infomation of the city or state
            - Name: Chinese name of the city or state
            - StateName: Chinese name of the state(if state, this does not exist)
            - CountryName: Chinese name of the country
        - ENInfo_dict: English infomation of the city or state
            - Refer to CNInfo_dict
        """
        try:
            city_list = []
            # keep track of the state
            state = set()
            with open(WeatherAssistant.ALL_CITY, 'r', encoding='utf-8') as f:
                # skip the first line
                next(f)
                # Data come this order: EnglishName,
                # ChineseName,StateName,StateNameEn,CountryName,CountryNameEn
                # store the data in a 3-tuple: (EnglishName, CNInfo_dict, ENInfo_dict)
                for line in f:
                    line = line.strip()
                    line = line.split(',')
                    temp = (line[1], {
                        'Name': line[0],
                        'StateName': line[2],
                        'CountryName': line[4]
                    }, {
                        'Name': line[1],
                        'StateName': line[3],
                        'CountryName': line[5]
                    })
                    # add state to city list
                    if temp[1]['StateName'] and temp[1]['StateName'] not in state:
                        state.add(temp[1]['StateName'])
                        temp_province = (temp[1]['StateName'], {
                            'Name': temp[1]['StateName'],
                            'CountryName': temp[1]['CountryName']
                        }, {
                            'Name': temp[2]['StateName'],
                            'CountryName': temp[2]['CountryName']
                        })
                        city_list.append(temp_province)
                    
                    city_list.append(temp)
            return city_list
        except:
            return []

    def save_cities(self):
        """
        Save cities to city file
        """
        try:
            with open(WeatherAssistant.CITIES_FILE, 'w') as f:
                for city in self.cities:
                    f.write(city + '\n')
        except:
            pass
    
    def add_city(self, city_name: str):
        """
        Add a city to city list
        """
        try:
            if city_name not in [city[0] for city in self.all_city_list]:
                return "Unknown city"
            if city_name in self.cities:
                return "City already in city list"
            self.cities.append(city_name)
            res = self.shift_city(city_name)
            if res != "Success":
                self.cities.pop()
                return res
            self.save_cities()
            return "Success"
        except:
            self.cities.pop()
            return "Unknown error"

    def remove_city(self, city_name: str):
        """
        Remove a city from city list
        """
        try:
            idx = self.cities.index(city_name)
            if idx != -1:
                self.cities.remove(city_name)
                if len(self.cities) == 0:
                    self.current_city = None
                    self.update_weather()
                else:
                    res = self.shift_city(self.cities[idx % len(self.cities)])
                    if res != "Success":
                        self.cities.append(city_name)
                        return res
            self.save_cities()
            return "Success"
        except:
            return "Unknown error"

    def shift_city(self, city_name: str):
        """
        Shift current city
        """
        try:
            if city_name not in self.cities:
                return "City not in city list"
            self.current_city = city_name
            self.save_cities()
            self.update_weather()
            return "Success"
        except:
            return "Unknown error"

    def update_weather(self):
        """
        Update current and forecast weather
        """
        try:
            self.weather = self.EMPTY_WEATHER_DICT
            if self.current_city is None:
                # print("No city selected")
                return
            city = self.get_weather.get_hf_location(self.current_city)
            idx = city['id']
            lat = city['lat']
            lon = city['lon']

            # self.weather['now'] = self.get_weather.get_hf_current(id)
            # self.weather['7d'] = self.get_weather.get_hf_7days(id)
            # self.weather['24h'] = self.get_weather.get_hf_24hours(id)
            # self.weather['rain'] = self.get_weather.get_hf_rain(lat, lon)
            # self.weather['warning'] = self.get_weather.get_hf_warning(id)
            # self.weather['indices'] = self.get_weather.get_hf_indices(id)
            # self.weather['air'] = self.get_weather.get_hf_air(id)
            # self.weather['air_forecast'] = self.get_weather.get_hf_air_forecast(id)
            # # print("Update weather success")

            # Use multi-threading to speed up
            api_functions = [
                lambda: self.get_weather.get_hf_current(idx),
                lambda: self.get_weather.get_hf_7days(idx),
                lambda: self.get_weather.get_hf_24hours(idx),
                lambda: self.get_weather.get_hf_rain(lat, lon),
                lambda: self.get_weather.get_hf_warning(idx),
                lambda: self.get_weather.get_hf_indices(idx),
                lambda: self.get_weather.get_hf_air(idx),
                lambda: self.get_weather.get_hf_air_forecast(idx)
            ]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(lambda func: func(), api_functions))

            keys = ['now', '7d', '24h', 'rain', 'warning', 'indices', 'air', 'air_forecast']
            for i in range(len(results)):
                self.weather[keys[i]] = results[i]


        except Exception as e:
            # print(e)
            # print("Update weather failed")
            self.weather = self.EMPTY_WEATHER_DICT

if __name__ == '__main__':
    
    def print_weather(wa):
        if wa.weather['now'] is None:
            print('----------------------------------------')
            print('Current city:', wa.current_city)
            print('No weather infomation')
            print(wa.weather)
            print('----------------------------------------')
            return
        print('----------------------------------------')
        print('Current city:', wa.current_city)
        print('Current weather:', wa.weather['now']['now']['text'])
        print('Current temperature:', wa.weather['now']['now']['temp'])
        print('----------------------------------------')

    def print_city_list(wa):
        print('----------------------------------------')
        print(f'Cities: {wa.cities}')
        print(f'Current city: {wa.current_city}')
        print('----------------------------------------')

    wa = WeatherAssistant()
    print_weather(wa)
    wa.add_city('Fuxin')
    print_city_list(wa)
    wa.shift_city('Fuxin')
    print_weather(wa)
    wa.remove_city('Fuxin')
    print_city_list(wa)
    print_weather(wa)

