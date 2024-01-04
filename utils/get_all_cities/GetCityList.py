# GetCityList.py
# Description: Get city list from xml file
# By Monster Kid

import xml.etree.ElementTree as ET

def parse_xml(xml_file):
    """
    Parse xml file and return a list of dictionaries 
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    city_data = []

    # Iterate all the cities
    for country_region in root.findall('./CountryRegion'):
        country_name = country_region.get('Name')
        country_code = country_region.get('Code')

        for state in country_region.findall('./State'):
            state_name = state.get('Name')
            state_code = state.get('Code')

            for city in state.findall('./City'):
                city_name = city.get('Name')
                city_code = city.get('Code')

                # Append the city data
                city_data.append({
                    'CountryName': country_name,
                    'CountryCode': country_code,
                    'StateName': state_name,
                    'StateCode': state_code,
                    'CityName': city_name,
                    'CityCode': city_code
                })

    return city_data

def match_city_names(xml_data1, xml_data2):
    """
    Match city names from two xml files
    """

    city_names = []

    # Iterate all the cities
    for city1 in xml_data1:
        for city2 in xml_data2:

            # Match the city
            if city1['CityCode'] == city2['CityCode']\
                and city1['StateCode'] == city2['StateCode']\
                and city1['CountryCode'] == city2['CountryCode']:
                city_names.append({
                    'ChineseName': city1['CityName'],
                    'EnglishName': city2['CityName'],
                    'StateName': city1['StateName'],
                    'StateNameEn': city2['StateName'], # 'StateNameEn' is not a good name, but I don't want to change it
                    'CountryName': city1['CountryName'],
                    'CountryNameEn': city2['CountryName'] # 'CountryNameEn' is not a good name, but I don't want to change it
                })

    return city_names

if __name__ == "__main__":
    xml_file1 = "LocList2.xml"
    xml_file2 = "LocList1.xml"

    # Parse the xml files
    chinese_data = parse_xml(xml_file1)
    english_data = parse_xml(xml_file2)

    # Match the city names
    city_names = match_city_names(chinese_data, english_data)

    # Store the list in a csv file
    csv_file = "city_list.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("ChineseName,EnglishName,StateName,StateNameEn,CountryName,CountryNameEn\n")
        for city in city_names:
            f.write(f"{city['ChineseName']},{city['EnglishName']},{city['StateName']},{city['StateNameEn']},{city['CountryName']},{city['CountryNameEn']}\n")
