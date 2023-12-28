# Interface.py
# Description: GUI of the program
# By Monster Kid

import tkinter as tk
import tkinter.ttk as ttk
import os
import json
from tkinter import messagebox
from WeatherAssistant import WeatherAssistant
from predict_city import predict_city
from SerialPages import *
from multi_lang_dict import *

##########################################################################
# """
# GUI
# ------------------
# Menu
# |Searchbox|   [City name]                         |
# |         |  [Temperture Number]                  |
# |City list|  [Max / Min Temperture]               |
# |         |  [Weather]                            |
# |         |  [Forecast Weather, line chart]       |
# |         |  [Humidity|Wind|Pressure|Clouds]      |
# ------------------
# - When searchbox is selected, the city list is disabled
# - When there's text in searchbox, below the searchbox are prediction cities
# """
# TODO:
# [x] WeatherAssistant Class, the controller of the program
# [x] Register API key
# [x] GetWeather Class to get weather infomation
# [x] Format the returned weather infomation
# [x] Interface Class, the view of the program
# [x] Add city list, including a lot of cities in the world
# [x] City prediction function, to predict the city name when user is typing
# [x] Version control, git
# [x] Forecast weather, line chart
# [x] Multi-language support
# [DNF] Icon and background color
# [x] Min max temperature(currently not correct)
# [x] Style and layout, font, color, etc. Window size, alignment, etc.
# [] Do not block the interface. Use multithreading and add a loading animation
# [x] Error handling, when the city is not found, etc.
# [] Up to date weather infomation
# [] Detailed Comments, Report
##########################################################################

class Interface(object):

    SETTING_PATH = "data/settings.json"
    DEFAULT_SETTINGS = {
        "language": "English",
    }
    def __init__(self, master):

        ## ----- Settings ----- ##
        self.settings = self.load_settings()
        self.weather_assistant = WeatherAssistant(language=language_alias_dict[self.settings["language"]])

        ## ----- Master ----- ##
        self.master = master
        self.master.title(language_dict[self.settings["language"]]["title"])
        self.width = 800
        self.height = 600
        self.master.geometry("{}x{}".format(self.width, self.height))
        self.master.resizable(False, False)
        self.master.bind('<Button-1>', self.on_background_click)
        self.master.bind('<Return>', self.on_master_return)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        
        ## ----- Menu ----- ##
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.create_menu()

        ## ----- Background ----- ##
        # The background is a frame
        self.background_frame = ttk.Frame(master)
        self.background_frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
    
        # Configure columns and rows
        self.left_frame_ratio = 1 / 6
        self.right_frame_ratio = 1 - self.left_frame_ratio
        
        ## ----- Left side ----- ##
        self.left_frame = ttk.Frame(self.background_frame)
        # Use place layout manager to place the left frame
        self.left_frame.place(relx=0, rely=0, relwidth=self.left_frame_ratio, relheight=1)
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, weight=0)
        self.left_frame.rowconfigure(1, weight=1)
        # Search bar and City list on the left
        # Do not use Helvetica font, use more common font
        # Ok I give in, use Helvetica font
        self.city_entry = tk.Entry(self.left_frame, font=("Helvetica", 16))
        self.city_entry.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        # When the searchbox is selected, the city list is disabled
        self.city_entry_var = tk.StringVar()
        self.city_entry_var.trace_add('write', self.update_city_listbox)
        self.city_entry.config(textvariable=self.city_entry_var)
        self.city_entry.bind('<FocusIn>', self.searchbox_selected)
        self.city_entry.bind('<FocusOut>', self.searchbox_unselected)
        # When there's text in searchbox, below the searchbox are prediction cities
        # The city listbox
        self.city_listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE)
        self.city_listbox.bind('<Double-Button-1>', self.city_listbox_click)
        self.city_listbox.grid(row=1, column=0, rowspan=4, sticky=tk.N+tk.S+tk.W+tk.E)
        self.city_listbox_status = "city_list"
        self.city_listbox.bind('<FocusIn>', self.city_listbox_selected)
        self.city_listbox.bind('<FocusOut>', self.city_listbox_unselected)
        self.prediction_list = []

        ## ----- Right side ----- ##
        self.right_frame = ttk.Frame(self.background_frame)
        # self.right_frame.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W+tk.E)
        self.right_frame.place(relx=self.left_frame_ratio, rely=0, relwidth=self.right_frame_ratio, relheight=1)
        # PLACE all the widgets in the right frame
        self.rf_weights = [1, 2, 1, 1, 1, 3, 5]
        self.rf_ratios = [weight / sum(self.rf_weights) for weight in self.rf_weights]
        # City name and delete city button
        self.city_name_label = tk.Label(self.right_frame, text=self.weather_assistant.current_city)
        self.city_name_label.place(relx=0, rely=0, relwidth=1, relheight=self.rf_ratios[0])
        # Current Temperature
        # Style: Big font
        self.current_temperature_label = tk.Label(self.right_frame, text="0", font=("Helvetica", 48))
        self.current_temperature_label.place(relx=0, rely=self.rf_ratios[0], relwidth=1, relheight=self.rf_ratios[1])
        # Max / Min Temperature
        self.max_min_temperature_label = tk.Label(self.right_frame, text="0/0")
        self.max_min_temperature_label.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1], relwidth=1, relheight=self.rf_ratios[2])
        # Current Weather
        self.current_weather_label = tk.Label(self.right_frame, text="Weather")
        self.current_weather_label.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1]+self.rf_ratios[2], relwidth=1, relheight=self.rf_ratios[3])
        # Warning scrollbox
        self.warning_scrollbox = SerialDisplay(self.right_frame, language=self.settings["language"])
        self.warning_scrollbox.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1]+self.rf_ratios[2]+self.rf_ratios[3], relwidth=1, relheight=self.rf_ratios[4])
        # Weather scrollbox 
        self.weather_scrollbox = SerialDisplay(self.right_frame)
        self.now_weather_page = NowWeatherPage(self.weather_scrollbox, language=self.settings["language"])
        self.air_page = AirPage(self.weather_scrollbox, language=self.settings["language"])
        self.index_page = IndexPage(self.weather_scrollbox, language=self.settings["language"])
        self.sun_moon_page = SunMoonPage(self.weather_scrollbox, language=self.settings["language"])
        self.wind_page = WindPage(self.weather_scrollbox, language=self.settings["language"])
        self.weather_scrollbox.add_page(self.now_weather_page)
        self.weather_scrollbox.add_page(self.air_page)
        self.weather_scrollbox.add_page(self.index_page)
        self.weather_scrollbox.add_page(self.sun_moon_page)
        self.weather_scrollbox.add_page(self.wind_page)
        self.weather_scrollbox.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1]+self.rf_ratios[2]+self.rf_ratios[3]+self.rf_ratios[4], relwidth=1, relheight=self.rf_ratios[5])
        # Chart scrollbox
        self.chart_scrollbox = SerialDisplay(self.right_frame, language=self.settings["language"])
        self.chart_24hours_page = Chart24HoursPage(self.chart_scrollbox, language=self.settings["language"])
        self.chart_7days_page = Chart7DaysPage(self.chart_scrollbox, language=self.settings["language"])
        self.chart_rain_page = ChartRainPage(self.chart_scrollbox, language=self.settings["language"])
        self.chart_scrollbox.add_page(self.chart_24hours_page)
        self.chart_scrollbox.add_page(self.chart_7days_page)
        self.chart_scrollbox.add_page(self.chart_rain_page)
        self.chart_scrollbox.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1]+self.rf_ratios[2]+self.rf_ratios[3]+self.rf_ratios[4]+self.rf_ratios[5], relwidth=1, relheight=self.rf_ratios[6])

        # Finalizing the layout
        self.master.focus()
        self.master.update()
        self.update()

    ## ----- Callback functions ----- ##

    def on_background_click(self, event):
        # When click on the background, the searchbox loses focus
        if event.widget != self.city_entry and event.widget != self.city_listbox:
            self.master.focus()
    
    def on_master_return(self, event):
        if self.city_listbox_status == "predict_list":
            # add the selected city to the city list
            self.add_city(self.prediction_list[0]["en"]["Name"])

    def searchbox_selected(self, event):
        self.city_listbox_status = "predict_list"
        self.update_city_listbox()

    def searchbox_unselected(self, event):
        # if listbox has focus, do nothing
        if self.master.focus_get() != self.city_listbox:
            self.city_listbox_status = "city_list"
            self.update_city_listbox()

    def city_listbox_selected(self, event):
        return
    
    def city_listbox_unselected(self, event):
        # if searchbox has focus, do nothing
        if self.master.focus_get() != self.city_entry:
            self.city_listbox_status = "city_list"
            self.update_city_listbox()
    
    def city_listbox_click(self, event):
        if self.city_listbox_status == "predict_list":
            # add the selected city to the city list
            self.add_city()
        else:
            # shift the selected city to the current city
            self.shift_city()

    ## ----- Functions ----- ##

    def create_menu(self):
        self.menu.delete(0, tk.END)
        # City
        self.city_menu = tk.Menu(self.menu)
        self.city_menu.add_command(label=language_dict[self.settings["language"]]["remove_city_command"], command=self.remove_city)
        self.menu.add_cascade(label=language_dict[self.settings["language"]]["city_menu"], menu=self.city_menu)
        # Settings
        self.settings_menu = tk.Menu(self.menu)
        self.settings_menu.add_command(label=language_dict[self.settings["language"]]["english_command"], command=lambda: self.change_language("English"))
        self.settings_menu.add_command(label=language_dict[self.settings["language"]]["chinese_command"], command=lambda: self.change_language("Chinese"))
        self.menu.add_cascade(label=language_dict[self.settings["language"]]["language_menu"], menu=self.settings_menu)
        # Help
        self.help_menu = tk.Menu(self.menu)
        self.help_menu.add_command(label=language_dict[self.settings["language"]]["help_menu"], command=lambda: messagebox.showinfo("About us", "Weather Assistant\nBy Monster Kid"))
        self.menu.add_cascade(label=language_dict[self.settings["language"]]["help_menu"], menu=self.help_menu)
    
    def save_settings(self):
        with open(self.SETTING_PATH, 'w') as f:
            json.dump(self.settings, f)
    
    def load_settings(self):
        if not os.path.exists(self.SETTING_PATH):
            return self.DEFAULT_SETTINGS
        with open(self.SETTING_PATH, 'r') as f:
            return json.load(f)

    def add_city(self, city=None):
        if city is None:
            city_idx = self.city_listbox.curselection()[0]
            city = list(self.weather_assistant.all_cities)[city_idx]
        res = self.weather_assistant.add_city(city)
        if res == "Success":
            self.update()
            messagebox.showinfo(language_dict[self.settings["language"]]["success"], \
                                language_dict[self.settings["language"]]["city_added"])
            # clear the searchbox
            self.city_entry.delete(0, tk.END)
            # remove focus from searchbox
            self.master.focus()
        else: 
            messagebox.showerror(language_dict[self.settings["language"]]["error"], res)

    def remove_city(self):
        res = self.weather_assistant.remove_city(self.weather_assistant.current_city)
        if res == "Success":
            self.update()
            messagebox.showinfo(language_dict[self.settings["language"]]["success"], \
                                language_dict[self.settings["language"]]["city_removed"])
        else:
            messagebox.showerror(language_dict[self.settings["language"]]["error"], res)

    def shift_city(self):
        # idx of city in city_listbox
        city_idx = self.city_listbox.curselection()[0]
        city = list(self.weather_assistant.cities)[city_idx]
        res = self.weather_assistant.shift_city(city)
        if res == "Success":
            self.update()
        else:
            messagebox.showerror(language_dict[self.settings["language"]]["error"], res)

    ## ----- Updating Functions ----- ##

    def update(self):
        self.update_weather()
        self.update_city_listbox()
        self.update_weather_scrollbox()
        self.update_chart_scrollbox()
        self.update_warnings()

    def update_weather(self):
        # Update current weather
        self.clear_all_labels()
        self.city_name_label.config(text=self.weather_assistant.all_cities[self.weather_assistant.current_city][language_alias_dict[self.settings["language"]]]["Name"])
        if self.weather_assistant.weather['now'] == None:
            self.current_temperature_label.config(text=language_dict[self.settings["language"]]["update_failure"])
            self.current_weather_label.config(text=language_dict[self.settings["language"]]["update_failure"])
        else:
            self.current_temperature_label.config(text=str(int(self.weather_assistant.weather['now']['now']['temp'])) + "°C")
            self.current_weather_label.config(text=self.weather_assistant.weather['now']['now']['text'])

        if self.weather_assistant.weather['7d'] == None:
            self.max_min_temperature_label.config(text=language_dict[self.settings["language"]]["update_failure"])
        else:
            self.max_min_temperature_label.config(text=str(int(self.weather_assistant.weather['7d']['daily'][0]['tempMin'])) + "°C / " + str(int(self.weather_assistant.weather['7d']['daily'][0]['tempMax'])) + "°C")
    
    def update_warnings(self):
        if self.weather_assistant.weather['warning'] == None:
            return
        data = self.weather_assistant.weather['warning']['warning']
        self.warning_scrollbox.clear()
        if len(data) == 0:
            no_warning_page = WarningPage(self.warning_scrollbox, language_dict[self.settings["language"]]["no_warning"])
            self.warning_scrollbox.add_page(no_warning_page)
        else:
            for warning in data:
                warning_page = WarningPage(self.warning_scrollbox, warning["title"])
                self.warning_scrollbox.add_page(warning_page) 
    
    def update_weather_scrollbox(self):
        # Update now weather page
        if self.weather_assistant.weather['now'] == None or self.weather_assistant.weather['now']['now'] == None:
            self.now_weather_page.clear()
        else:
            self.now_weather_page.update(**self.weather_assistant.weather['now']['now'])
        # Update wind page
        if self.weather_assistant.weather['now'] == None or self.weather_assistant.weather['now']['now'] == None:
            self.wind_page.clear()
        else:
            self.wind_page.update(**self.weather_assistant.weather['now']['now'])
        # Update index page
        if self.weather_assistant.weather['indices'] == None:
            self.index_page.clear()
        else:
            self.index_page.update(**self.weather_assistant.weather['indices'])
        # Update air page
        if self.weather_assistant.weather['air'] == None:
            self.air_page.clear()
        else:
            self.air_page.update(**self.weather_assistant.weather['air']['now'])
        # Update sun moon page
        if self.weather_assistant.weather['7d'] == None:
            self.sun_moon_page.clear()
        else:
            self.sun_moon_page.update(**self.weather_assistant.weather['7d']['daily'][0])
    
    def update_chart_scrollbox(self):
        # Update 24 hours chart page
        if self.weather_assistant.weather['24h'] == None:
            self.chart_24hours_page.clear()
        else:
            self.chart_24hours_page.update(**self.weather_assistant.weather['24h'])
        # Update 7 days chart page
        if self.weather_assistant.weather['7d'] == None:
            self.chart_7days_page.clear()
        else:
            self.chart_7days_page.update(**self.weather_assistant.weather['7d'])
        # Update rain chart page
        if self.weather_assistant.weather['rain'] == None:
            self.chart_rain_page.clear()
        else:
            self.chart_rain_page.update(**self.weather_assistant.weather['rain'])
    
    def clear_all_labels(self):
        self.city_name_label.config(text="")
        self.current_temperature_label.config(text="")
        self.max_min_temperature_label.config(text="")
        self.current_weather_label.config(text="")
    
    def update_city_listbox(self, *args):
        self.prediction_list = []
        if self.city_listbox_status == "predict_list":
            # delete all the items from the listbox
            self.city_listbox.delete(0, tk.END)
            # predict the city name
            text = self.city_entry.get()
            self.prediction_list = predict_city(text, self.weather_assistant.all_cities, language=self.settings["language"])
            for city in self.prediction_list:
                display = city[language_alias_dict[self.settings["language"]]]["Name"]
                self.city_listbox.insert(tk.END, display)
        else:
            self.city_listbox.delete(0, tk.END)
            for city in self.weather_assistant.cities:
                display = self.weather_assistant.all_cities[city][language_alias_dict[self.settings["language"]]]["Name"]
                self.city_listbox.insert(tk.END, display)
    
    def change_language(self, language):
        self.settings["language"] = language
        self.save_settings()

        self.master.title(language_dict[self.settings["language"]]["title"])
        self.create_menu()
        self.weather_assistant.set_language(language_alias_dict[self.settings["language"]])

        self.weather_scrollbox.set_language(self.settings["language"])
        self.warning_scrollbox.set_language(self.settings["language"])
        self.chart_scrollbox.set_language(self.settings["language"])

        self.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()

