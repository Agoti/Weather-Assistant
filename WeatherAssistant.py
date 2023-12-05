# WeatherAssistant.py
# Description: Weather Assistant class to manage weather infomation
#     This is the controller of the program
# By Monster Kid
from getWeather import *

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

    def __init__(self):
        self.GetWeather = GetWeather()
        self.current_weather = None
        self.forecast_weather = None
        self.cities, self.current_city = self.load_cities()
        self.all_city_list = self.load_all_city()
        self.update_weather()
    
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
            if self.current_city is None:
                self.current_weather = None
                self.forecast_weather = None
            else:
                self.current_weather = self.GetWeather.get_current_weather(self.current_city)
                self.forecast_weather = self.GetWeather.get_forecast_weather(self.current_city)
        except:
            self.current_weather = None
            self.forecast_weather = None


if __name__ == '__main__':
    
    def print_weather(wa):
        if wa.current_weather is None:
            print('----------------------------------------')
            print('Current city:', wa.current_city)
            print('No weather infomation')
            print('----------------------------------------')
            return
        print('----------------------------------------')
        print('Current city:', wa.current_city)
        weather = wa.current_weather[2]['weather']['main']
        main = wa.current_weather[2]['main']
        print('Weather:', weather)
        print(f'Temperature: {int(main["temp"] - 273.15)}')
        print('Humidity:', main['humidity'])
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

