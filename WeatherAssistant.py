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
    # the file to store all cities (around the world)
    ALL_CITY = 'data/all_city.csv'
    # empty weather information dictionary
    EMPTY_WEATHER_DICT = {'now' : None, '7d' : None, '24h' : None, 'rain' : None, 'warning' : None, 'indices' : None,
                      'air' : None, 'air_forecast' : None}

    def __init__(self, language: str = 'en', do_not_update: bool = False):
        """
        Initialize WeatherAssistant
            :param language: language of the weather infomation
            :param do_not_update: whether to update weather infomation after initialization
        """
    
        # Initialize GetWeather
        self.get_weather = GetWeather(language)
        # set language of self and get_weather
        self.language = language
        self.set_language(language)
        # load city list
        self.cities, self.current_city = self.load_cities()
        # load all cities
        self.all_cities = self.load_all_cities()
        # initialize weather information
        self.weather = self.EMPTY_WEATHER_DICT
        # update weather information
        if not do_not_update:
            self.update_weather()

    def set_language(self, language: str):
        """
        Set language
        """
        try:
            # set new language
            self.language = language
            # set language of get_weather
            self.get_weather.set_hf_language(language)
            # update weather, since language changed
            self.update_weather()

            return "success"
        except ValueError as e:
            return str(e)
        except:
            return "unknown_error"

    
    def load_cities(self) -> tuple:
        """
        Load cities from city file
        """
        try:
            # cities: a list of cities which user added
            cities = []
            # current_city: the current city whose weather is displayed
            current_city = None
            # read cities from cities file
            with open(WeatherAssistant.CITIES_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    city = line.strip()
                    cities.append(city)
                    if current_city is None:
                        current_city = city

            return cities, current_city
        except:
            return [], None

    def load_all_cities(self) -> dict:
        """
        Load all cities from csv file
        all_cities: a dict {en_name: {'en': en_dict, 'zh': cn_dict}}
        - en_name: English name of the city
        - cn_dict: Chinese infomation of the city or state
            - Name: Chinese name of the city or state
            - StateName: Chinese name of the state(if state, this does not exist)
            - CountryName: Chinese name of the country
        - en_dict: English infomation of the city or state
            - Refer to cn_dict
        """
        try:
            # all_cities: a dict {en_name: {'en': en_dict, 'zh': cn_dict}}
            cities = {}
            # keep track of the state
            state = set()
            # read cities from all cities file
            with open(WeatherAssistant.ALL_CITY, 'r', encoding='utf-8') as f:
                # skip the first line
                next(f)
                # Data come this order: EnglishName,
                # ChineseName,StateName,StateNameEn,CountryName,CountryNameEn
                # Decode the line and add to all_cities
                for line in f:
                    line = line.strip()
                    line = line.split(',')
                    temp = {'zh': {
                        'Name': line[0],
                        'StateName': line[2],
                        'CountryName': line[4]
                    }, 'en': {
                        'Name': line[1],
                        'StateName': line[3],
                        'CountryName': line[5]
                    }, 'type': 'city'}
                    # if state is not tracked, add it to all_cities
                    if temp['zh']['StateName'] and temp['zh']['StateName'] not in state:
                        state.add(temp['zh']['StateName'])
                        temp_province = {
                            'zh': {
                                'Name': temp['zh']['StateName'],
                                'CountryName': temp['zh']['CountryName']
                            },
                            'en': {
                                'Name': temp['en']['StateName'],
                                'CountryName': temp['en']['CountryName']
                        }, 'type': 'state'}
                        cities[temp['en']['StateName']] = temp_province
                    
                    cities[temp['en']['Name']] = temp

            return cities
        except Exception as e:
            print(e)
            return {}

    def save_cities(self):
        """
        Save cities to city file
        """
        try:
            # write cities to cities file
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
            # check if city_name is valid
            if city_name not in self.all_cities:
                return "unknown_city"
            # check if city_name is already in city list
            if city_name in self.cities:
                return "city_in_list"
            # add it to city list
            self.cities.append(city_name)
            # shift to the new city
            res = self.shift_city(city_name)
            # if shift failed, remove the city from city list
            if res != "success":
                self.cities.pop()
                return res
            # save city list to file
            self.save_cities()

            return "success"
        except:
            return "unknown_error"

    def remove_city(self, city_name: str):
        """
        Remove a city from city list
        """
        try:
            # check if city_name is None
            if city_name is None:
                return "no_city"
            # get the index of city_name in city list
            idx = self.cities.index(city_name)
            # if city_name is in city list, remove it
            if idx != -1:
                self.cities.remove(city_name)
                # shift to the next city and update weather
                # check if the last city is removed
                if len(self.cities) == 0:
                    self.current_city = None
                    self.update_weather()
                else:
                    res = self.shift_city(self.cities[idx % len(self.cities)])
                    if res != "success":
                        self.cities.append(city_name)
                        return res

            # save city list to file
            self.save_cities()

            return "success"

        except Exception as e:
            return "unknown_error"

    def shift_city(self, city_name: str):
        """
        Shift current city
        """
        try:
            # check if city_name is in city list
            if city_name not in self.cities:
                return "city_not_in_list"
            # update current city, file and weather
            self.current_city = city_name
            self.save_cities()
            self.update_weather()

            return "success"
        except:
            return "unknown_error"

    def update_weather(self):
        """
        Update current and forecast weather
        """
        try:
            # reset weather dict
            self.weather = self.EMPTY_WEATHER_DICT

            # check if current city is None
            if self.current_city is None:
                return

            # get city id, latitude and longitude
            city = self.get_weather.get_hf_location(self.current_city)
            if city is None:
                return self.EMPTY_WEATHER_DICT
            idx = city['id']
            lat = city['lat']
            lon = city['lon']

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

            # Execute all api functions
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(lambda func: func(), api_functions))

            # Update weather dict
            keys = ['now', '7d', '24h', 'rain', 'warning', 'indices', 'air', 'air_forecast']
            for i in range(len(results)):
                self.weather[keys[i]] = results[i]

        except Exception as e:
            self.weather = self.EMPTY_WEATHER_DICT


# Test
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

