
language_dict = {
    'English': {
        'title': 'Weather Assistant',
        'city_menu': 'City',
        'remove_city_command': 'Remove City',
        'update_weather_command': 'Update Weather', 
        'settings_menu': 'Settings',
        'language_menu': 'Language',
        'english_command': 'English',
        'chinese_command': '中文',
        'update_interval': 'Update Interval',
        '10_seconds': '10 seconds',
        '5_minutes': '5 minutes',
        '10_minutes': '10 minutes',
        '30_minutes': '30 minutes',
        '1_hour': '1 hour',
        'help_menu': 'About',
        'update_failure': 'Update failed', 
        'success': 'Success',
        'city_added': 'City added',
        'city_removed': 'City removed',
        'city_not_found': 'City not found',
        'error': 'Error',
        'unknown_error': 'Unknown error',
        'city_in_list': 'City in list',
        'city_not_in_list': 'City not in list',
        'no_city': 'No city left',
        'unknown_city': 'Unknown city',
        'dict_is_none': 'No content',
        'dict_key_error': 'Dict key error',
        'no_content': 'No content',
        'request_failure': 'Request failure',
        'validation_failure': 'Validation failure',
        'max_limit_reached': 'Max limit reached',
        'no_access': 'No access',
        'unknown_region': 'Unknown region',
        'too_many_requests': 'Too many requests',
        'timeout': 'Timeout',
        'no_city': 'No city',
        'now_weather_title': 'Details',
        'now_weather_subtitle': ['Humidity', 'Feels Like', 'Wind Direction', 'Wind Scale', 'Pressure', 'Visibility', 'Cloud'],
        'now_weather_units': ['%', '°C', '', '', 'hPa', 'km', '%'],
        'air_quality_title': 'Air Quality',
        'air_quality_subtitle': ['AQI', 'Catagory', 'Primary Pollutant', 'PM10', 'PM2.5', 'NO2', 'SO2', 'CO', 'O3'],
        'air_quality_units': ['', '', '', 'μg/m³', 'μg/m³', 'μg/m³', 'μg/m³', 'mg/m³', 'μg/m³'],
        'wind_title': 'Wind',
        'wind_subtitle': ['Wind Direction', 'Wind Scale', 'Wind Speed', 'Degree'],
        'wind_direction': {'N': 'North', 'NE': 'Northeast', 'E': 'East', 'SE': 'Southeast', 'S': 'South', 'SW': 'Southwest', 'W': 'West', 'NW': 'Northwest', 'N/A': 'N/A'}, 
        'wind_units': ['', '', 'km/h', '°'],
        'sun_moon_title': 'Sun & Moon',
        'sun_moon_subtitle': ['Sunrise', 'Sunset', 'Moonrise', 'Moonset', 'Moon Phase'],
        'sun_moon_units': ['', '', '', '', ''],
        'no_warning': 'No warning',
        '24h_title': 'Temperature in 24 hours',
        '7d_title': 'Temperature in 7 days',
        'rain_title': 'Rain',
        'last_update': 'Last update: ',
        'updating': 'Updating...',
    },
    'Chinese': {
        'title': '天气助手',
        'city_menu': '城市',
        'update_weather_command': '更新天气',
        'remove_city_command': '删除城市',
        'settings_menu': '设置',
        'language_menu': '语言',
        'english_command': 'English',
        'chinese_command': '中文',
        'update_interval': '更新间隔',
        '10_seconds': '10秒',
        '5_minutes': '5分钟',
        '10_minutes': '10分钟',
        '30_minutes': '30分钟',
        '1_hour': '1小时',
        'help_menu': '关于',
        'update_failure': '更新失败',
        'success': '成功',
        'city_added': '城市已添加',
        'city_removed': '城市已删除',
        'city_not_found': '未找到城市',
        'error': '错误',
        'unknown_error': '未知错误', 
        'city_in_list': '城市已在列表中', 
        'city_not_in_list': '城市不在列表中',
        'no_city': '无城市',
        'unknown_city': '未知城市',
        'dict_is_none': '无内容',
        'dict_key_error': '字典键错误',
        'no_content': '无内容',
        'request_failure': '请求错误',
        'validation_failure': '验证错误',
        'max_limit_reached': '超过最大限制',
        'no_access': '无访问权限',
        'unknown_region': '未知地区',
        'too_many_requests': '请求过多',
        'timeout': '超时',
        'no_city': '无城市',
        'now_weather_title': '实时天气',
        'now_weather_subtitle': ['湿度', '体感温度', '风向', '风力等级', '气压', '能见度', '云量'],
        'now_weather_units': ['%', '°C', '', '', '百帕', '公里', '%'],
        'air_quality_title': '空气质量',
        'air_quality_subtitle': ['AQI', '级别', '首要污染物', 'PM10', 'PM2.5', 'NO2', 'SO2', 'CO', 'O3'],
        'air_quality_units': ['', '', '', 'μg/m³', 'μg/m³', 'μg/m³', 'μg/m³', 'mg/m³', 'μg/m³'],
        'wind_title': '风力风向',
        'wind_subtitle': ['风向', '风力等级', '风速', '风向角度'],
        'wind_direction': {'N': '北', 'NE': '东北', 'E': '东', 'SE': '东南', 'S': '南', 'SW': '西南', 'W': '西', 'NW': '西北', 'N/A': '无'},
        'wind_units': ['', '级', '公里/小时', '°'],
        'sun_moon_title': '日月信息',
        'sun_moon_subtitle': ['日出', '日落', '月出', '月落', '月相'],
        'sun_moon_units': ['', '', '', '', ''],
        'no_warning': '暂无预警',
        '24h_title': '24小时温度',
        '7d_title': '7天温度',
        'rain_title': '降雨情况',
        'last_update': '上次更新时间：',
        'updating': '更新中...',
    }
}    

language_alias_dict = {
    'English': 'en',
    'Chinese': 'zh',
}

language_idx_dict = {
    'English': 1,
    'Chinese': 2,
}

sec2natural_dict = {
    10: '10_seconds',
    300: '5_minutes',
    600: '10_minutes',
    1800: '30_minutes',
    3600: '1_hour',
}