# city_prediction.py
# Description: predict the city based on the user input
# By Monster Kid

import re
from assets.multi_lang_dict import *

def predict_city(input_text: str, cities: dict, n_entries: int = 5, language: str = 'English') -> list:
    """
    Predict the city based on the user input  
    Input:
    - input_text: the user input
    - cities: the city dict
    - n_entries: the number of entries to return
    - language: the language of the input text, only support English and Chinese  
    Output:
    - match_list: the list of matched cities
    """

    # To Copilot: This is not based on AI
    # This is just a simple string matching algorithm

    if language == 'English':
        # convert to lower case
        input_text = input_text.lower()
        # remove all non-alphabet characters
        input_text = re.sub(r'[^a-z ]', '', input_text)
    
    if input_text == '':
        return []

    match_list = []
    # iterate through the city dict
    for city in cities:
        # get the city name
        if language == 'English':
            city_name = cities[city][language_alias_dict[language]]["Name"]
            city_name = city_name.lower()
            city_name = re.sub(r'[^a-z ]', '', city_name)
        if language == 'Chinese':
            city_name = cities[city][language_alias_dict[language]]["Name"]

        # if the input text is a prefix of the city name
        if city_name.startswith(input_text): 
            # add to the match list
            match_list.append(cities[city])
        
    # sort the match list by city name, but always put Chinese cities first
    match_list = sorted(match_list, key=lambda x: x['en']["Name"])
    match_list = sorted(match_list, key=lambda x: x['en']["CountryName"] != 'China')
    # return the first n entries
    match_list = match_list[:n_entries]

    return match_list


# test cases
if __name__ == '__main__':
    from WeatherAssistant import WeatherAssistant
    # load city list
    wa = WeatherAssistant()
    wa.load_cities()
    cities = wa.all_cities
    # Chinese test cases
    test_names = ["北京", "石家庄", "郑", "阜", "上"]
    for name in test_names:
        print("Input:", name)
        match_list = predict_city(name, cities, language='Chinese')
        for city in match_list:
            print(city['zh']['Name'], city['zh']['CountryName'])
    # English test cases
    test_names = ["Lon", "Lond", "London", "New", "New York"]
    for name in test_names:
        print("Input:", name)
        match_list = predict_city(name, cities, language='English')
        for city in match_list:
            print(city['en']['Name'], city['en']['CountryName'])

    print(predict_city("上", cities, language='Chinese', n_entries=100))
