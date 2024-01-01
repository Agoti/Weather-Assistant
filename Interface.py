# Interface.py
# Description: GUI of the program
# By Monster Kid

import tkinter as tk
import tkinter.ttk as ttk
import os
import json
import time
import threading
import warnings
from tkinter import messagebox
from WeatherAssistant import WeatherAssistant
from utils.predict_city import predict_city
from utils.SerialPages import *
from assets.multi_lang_dict import *
from utils.TimerThread import TimerThread

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
# [x] Do not block the interface. Use multithreading and add a loading animation
# [x] Error handling, when the city is not found, etc.
# [x] Up to date weather infomation
# [Soon] Detailed Comments, Report
##########################################################################

class Interface(object):

    SETTING_PATH = "data/settings.json"
    DEFAULT_SETTINGS = {
        "language": "English",
        "update_interval": 300, 
    }
    def __init__(self, master):

        ## ----- Settings ----- ##
        self.settings = self.load_settings()
        self.weather_assistant = WeatherAssistant(language=language_alias_dict[self.settings["language"]])

        ## ----- Threads ----- ##
        self.thread_lock = threading.Lock()
        # Timer thread
        self.timer_thread = TimerThread(self.settings["update_interval"], self.update_weather)

        ## ----- Master ----- ##
        self.master = master
        self.master.title(language_dict[self.settings["language"]]["title"])
        self.width = 800
        self.height = 700
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
        # Do not use Helvetica font, use a Chinese-friendly font
        self.city_entry = ttk.Entry(self.left_frame, font=("Microsoft YaHei", 12))
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
        self.rf_weights = [1, 2, 1, 1, 1, 3, 8, 1]
        self.rf_ratios = [weight / sum(self.rf_weights) for weight in self.rf_weights]
        # City name and delete city button
        self.city_name_label = tk.Label(self.right_frame, text=self.weather_assistant.current_city)
        self.city_name_label.place(relx=0, rely=0, relwidth=1, relheight=self.rf_ratios[0])
        # Current Temperature
        # Style: Big font
        self.current_temperature_label = tk.Label(self.right_frame, text="0", font=("Microsoft YaHei", 44))
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
        # Last update time
        self.last_update_time_label = tk.Label(self.right_frame, text=language_dict[self.settings["language"]]["last_update"])
        self.last_update_time_label.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1]+self.rf_ratios[2]+self.rf_ratios[3]+self.rf_ratios[4]+self.rf_ratios[5]+self.rf_ratios[6], relwidth=1, relheight=self.rf_ratios[7])

        # Finalizing the layout
        self.master.focus()
        self.master.update()
        self.update_ui()
        self.timer_thread.start()

    ## ----- Callback functions ----- ##

    def on_background_click(self, event):
        # When click on the background, the searchbox loses focus
        if event.widget != self.city_entry and event.widget != self.city_listbox:
            self.master.focus()
    
    def on_master_return(self, event):
        if self.city_listbox_status == "predict_list":
            # add the selected city to the city list
            if not self.prediction_list:
                return
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
            if self.city_listbox.curselection() == ():
                return
            selected_city_idx = self.city_listbox.curselection()[0]
            selected_city = self.prediction_list[selected_city_idx]["en"]["Name"]
            # add the selected city to the city list
            self.add_city(selected_city)
        else:
            # shift the selected city to the current city
            self.shift_city()

    ## ----- Functions ----- ##

    def create_menu(self):
        self.menu.delete(0, tk.END)
        # City
        self.city_menu = tk.Menu(self.menu, tearoff=False)
        self.city_menu.add_command(label=language_dict[self.settings["language"]]["remove_city_command"], command=self.remove_city)
        self.city_menu.add_command(label=language_dict[self.settings["language"]]["update_weather_command"], command=self.update_weather)
        self.menu.add_cascade(label=language_dict[self.settings["language"]]["city_menu"], menu=self.city_menu)
        # Settings
        self.settings_menu = tk.Menu(self.menu, tearoff=False)
        self.language_submenu = tk.Menu(self.settings_menu, tearoff=False)
        self.language_submenu.add_command(label=language_dict[self.settings["language"]]["english_command"], command=lambda: self.change_language("English"))
        self.language_submenu.add_command(label=language_dict[self.settings["language"]]["chinese_command"], command=lambda: self.change_language("Chinese"))
        self.update_interval_submenu = tk.Menu(self.settings_menu, tearoff=False)
        self.update_interval_submenu.add_command(label=language_dict[self.settings["language"]]["10_seconds"], command=lambda: self.change_update_interval(10))
        self.update_interval_submenu.add_command(label=language_dict[self.settings["language"]]["5_minutes"], command=lambda: self.change_update_interval(300))
        self.update_interval_submenu.add_command(label=language_dict[self.settings["language"]]["10_minutes"], command=lambda: self.change_update_interval(600))
        self.update_interval_submenu.add_command(label=language_dict[self.settings["language"]]["30_minutes"], command=lambda: self.change_update_interval(1800))
        self.update_interval_submenu.add_command(label=language_dict[self.settings["language"]]["1_hour"], command=lambda: self.change_update_interval(3600))
        self.menu.add_cascade(label=language_dict[self.settings["language"]]["settings_menu"], menu=self.settings_menu)
        self.settings_menu.add_cascade(label=language_dict[self.settings["language"]]["language_menu"], menu=self.language_submenu, underline=0)
        text_update_interval = language_dict[self.settings["language"]]["update_interval"] + ": " + \
                                 language_dict[self.settings["language"]][sec2natural_dict[self.settings["update_interval"]]]
        self.settings_menu.add_cascade(label=text_update_interval, menu=self.update_interval_submenu, underline=0)
        # Help
        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.help_menu.add_command(label=language_dict[self.settings["language"]]["help_menu"], command=lambda: messagebox.showinfo("About us", "Weather Assistant\nBy Monster Kid\nSupport: Hefeng Weather"))
        self.menu.add_cascade(label=language_dict[self.settings["language"]]["help_menu"], menu=self.help_menu)
    
    def save_settings(self):
        with open(self.SETTING_PATH, 'w') as f:
            json.dump(self.settings, f)
    
    def load_settings(self):
        if not os.path.exists(self.SETTING_PATH):
            return self.DEFAULT_SETTINGS
        with open(self.SETTING_PATH, 'r') as f:
            return json.load(f)
    
    def add_city(self, city):
        thread = threading.Thread(target=self.add_city_thread, args=(city,))
        thread.start()

    def add_city_thread(self, city=None):
        self.thread_lock.acquire()
        self.last_update_time_label.config(text=language_dict[self.settings["language"]]["updating"])
        # print(f"Adding city {city}")
        res = self.weather_assistant.add_city(city)
        if res == "success":
            self.update_ui()
            messagebox.showinfo(language_dict[self.settings["language"]]["success"], \
                                language_dict[self.settings["language"]]["city_added"])
            # clear the searchbox
            self.city_entry.delete(0, tk.END)
            # remove focus from searchbox
            self.master.focus()
        else: 
            messagebox.showerror(language_dict[self.settings["language"]]["error"], \
                                 language_dict[self.settings["language"]][res])
        self.thread_lock.release()
    
    def remove_city(self):
        thread = threading.Thread(target=self.remove_city_thread)
        thread.start()

    def remove_city_thread(self):
        self.thread_lock.acquire()
        self.last_update_time_label.config(text=language_dict[self.settings["language"]]["updating"])
        res = self.weather_assistant.remove_city(self.weather_assistant.current_city)
        # print(self.weather_assistant.current_city)
        # print(self.weather_assistant.weather == self.weather_assistant.EMPTY_WEATHER_DICT)
        if res == "success":
            self.update_ui()
            messagebox.showinfo(language_dict[self.settings["language"]]["success"], \
                                language_dict[self.settings["language"]]["city_removed"])
        else:
            messagebox.showerror(language_dict[self.settings["language"]]["error"], \
                                language_dict[self.settings["language"]][res])
        self.thread_lock.release()
    
    def shift_city(self):
        if self.city_listbox.curselection() == ():
            return
        city_idx = self.city_listbox.curselection()[0]
        city = list(self.weather_assistant.cities)[city_idx]
        thread = threading.Thread(target=self.shift_city_thread, args=(city,))
        thread.start()

    def shift_city_thread(self, city):
        self.thread_lock.acquire()
        self.last_update_time_label.config(text=language_dict[self.settings["language"]]["updating"])
        res = self.weather_assistant.shift_city(city)
        if res == "success":
            self.update_ui()
        else:
            messagebox.showerror(language_dict[self.settings["language"]]["error"], \
                                language_dict[self.settings["language"]][res])
        self.thread_lock.release()
    
    def update_weather(self):
        thread = threading.Thread(target=self.update_weather_thread)
        thread.start()
        
    def update_weather_thread(self):
        self.thread_lock.acquire()
        self.last_update_time_label.config(text=language_dict[self.settings["language"]]["updating"])
        self.weather_assistant.update_weather()
        self.update_ui()
        self.thread_lock.release()
    
    def handle_code(self, dict):
        if dict == None:
            return "0", "dict_is_none"
        code = dict["code"]
        err_dict = {
            "200": "success",
            "204": "no_content", 
            "400": "request_failure",
            "401": "validation_failure",
            "402": "max_limit_reached", 
            "403": "no_access",
            "404": "unknown_region",
            "429": "too_many_requests",
            "500": "timeout",
        }
        return code, err_dict[code]

    ## ----- Updating Functions ----- ##

    def update_ui(self):
        self.update_labels()
        self.update_city_listbox()
        self.update_weather_scrollbox()
        self.update_chart_scrollbox()
        self.update_warnings()

    def update_labels(self):
        # Update current weather
        self.clear_all_labels()
        if self.weather_assistant.current_city == None:
            self.city_name_label.config(text=language_dict[self.settings["language"]]["no_city"])
            return
        self.city_name_label.config(text=self.weather_assistant.all_cities[self.weather_assistant.current_city][language_alias_dict[self.settings["language"]]]["Name"])
        code, err = self.handle_code(self.weather_assistant.weather['now'])
        if code != "200":
            self.current_temperature_label.config(text=language_dict[self.settings["language"]][err])
            # self.current_weather_label.config(text=language_dict[self.settings["language"]]["update_failure"])
            # self.last_update_time_label.config(text=language_dict[self.settings["language"]]["update_failure"])
        else:
            self.current_temperature_label.config(text=str(int(self.weather_assistant.weather['now']['now']['temp'])) + "°C")
            self.current_weather_label.config(text=self.weather_assistant.weather['now']['now']['text'])
            # datetime string is ISO 8601 format
            parsed_time = time.strptime(self.weather_assistant.weather['now']['updateTime'], "%Y-%m-%dT%H:%M%z")
            text = language_dict[self.settings["language"]]["last_update"] + time.strftime("%Y-%m-%d %H:%M", parsed_time)
            text += " " + self.weather_assistant.weather['now']['refer']['sources'][0]
            text += " " + self.weather_assistant.weather['now']['refer']['license'][0]
            self.last_update_time_label.config(text=text)

        code, err = self.handle_code(self.weather_assistant.weather['7d'])
        if code != "200":
            # self.max_min_temperature_label.config(text=language_dict[self.settings["language"]][err])
            pass
        else:
            self.max_min_temperature_label.config(text=str(int(self.weather_assistant.weather['7d']['daily'][0]['tempMin'])) + "°C / " + str(int(self.weather_assistant.weather['7d']['daily'][0]['tempMax'])) + "°C")
    
    def update_warnings(self):
        self.warning_scrollbox.delete_all_pages()
        code, err = self.handle_code(self.weather_assistant.weather['warning'])
        if code != "200" or self.weather_assistant.weather['warning']['warning'] == None:
            error_page = WarningPage(self.warning_scrollbox, language_dict[self.settings["language"]][err])
            self.warning_scrollbox.add_page(error_page)
            return
        data = self.weather_assistant.weather['warning']['warning']
        if len(data) == 0:
            no_warning_page = WarningPage(self.warning_scrollbox, language_dict[self.settings["language"]]["no_warning"])
            self.warning_scrollbox.add_page(no_warning_page)
        else:
            for warning in data:
                warning_page = WarningPage(self.warning_scrollbox, warning["title"])
                self.warning_scrollbox.add_page(warning_page) 
    
    def update_weather_scrollbox(self):
        self.weather_scrollbox.clear()
        if self.weather_assistant.current_city == None:
            return
        # Update now weather page
        code, err = self.handle_code(self.weather_assistant.weather['now'])
        if code != "200":
            self.now_weather_page.clear()
        else:
            self.now_weather_page.update(**self.weather_assistant.weather['now']['now'])
        # Update wind page
        code, err = self.handle_code(self.weather_assistant.weather['now'])
        if code != "200" or self.weather_assistant.weather['now']['now'] == None:
            self.wind_page.clear()
        else:
            self.wind_page.update(**self.weather_assistant.weather['now']['now'])
        # Update index page
        code, err = self.handle_code(self.weather_assistant.weather['indices'])
        if code != "200":
            self.index_page.clear()
            self.index_page.update()
        else:
            self.index_page.update(**self.weather_assistant.weather['indices'])
        # Update air page
        code, err = self.handle_code(self.weather_assistant.weather['air'])
        if code != "200":
            self.air_page.clear()
        else:
            self.air_page.update(**self.weather_assistant.weather['air']['now'])
        # Update sun moon page
        code, err = self.handle_code(self.weather_assistant.weather['7d'])
        if code != "200":
            self.sun_moon_page.clear()
        else:
            self.sun_moon_page.update(**self.weather_assistant.weather['7d']['daily'][0])
    
    def update_chart_scrollbox(self):
        self.chart_scrollbox.clear()
        if self.weather_assistant.current_city == None:
            return
        code, err = self.handle_code(self.weather_assistant.weather['24h'])
        # Update 24 hours chart page
        if code != "200":
            self.chart_24hours_page.clear()
        else:
            self.chart_24hours_page.update(**self.weather_assistant.weather['24h'])
        # Update 7 days chart page
        code, err = self.handle_code(self.weather_assistant.weather['7d'])
        if code != "200":
            self.chart_7days_page.clear()
        else:
            self.chart_7days_page.update(**self.weather_assistant.weather['7d'])
        # Update rain chart page
        code, err = self.handle_code(self.weather_assistant.weather['rain'])
        if code != "200":
            self.chart_rain_page.clear()
        else:
            self.chart_rain_page.update(**self.weather_assistant.weather['rain'])
    
    def clear_all_labels(self):
        self.city_name_label.config(text="")
        self.current_temperature_label.config(text="")
        self.max_min_temperature_label.config(text="")
        self.current_weather_label.config(text="")
        self.last_update_time_label.config(text="")
    
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
                state = city[language_alias_dict[self.settings["language"]]]["StateName"] if city['type'] == 'city' else None
                country = city[language_alias_dict[self.settings["language"]]]["CountryName"]
                display += ", " + state if state is not None and state != "None" else ""
                self.city_listbox.insert(tk.END, display)
        else:
            self.city_listbox.delete(0, tk.END)
            for city in self.weather_assistant.cities:
                display = self.weather_assistant.all_cities[city][language_alias_dict[self.settings["language"]]]["Name"]
                self.city_listbox.insert(tk.END, display)
    
    ## ----- Settings Functions ----- ##

    def change_language(self, language):
        self.settings["language"] = language
        self.save_settings()

        self.master.title(language_dict[self.settings["language"]]["title"])
        self.create_menu()
        
        self.thread_lock.acquire()
        self.weather_assistant.set_language(language_alias_dict[self.settings["language"]])

        self.weather_scrollbox.set_language(self.settings["language"])
        self.warning_scrollbox.set_language(self.settings["language"])
        self.chart_scrollbox.set_language(self.settings["language"])

        self.update_ui()
        self.thread_lock.release()
    
    def change_update_interval(self, interval):
        self.settings["update_interval"] = interval
        self.save_settings()
        # kill the timer thread and restart it
        self.timer_thread.stop()
        self.timer_thread = TimerThread(self.settings["update_interval"], self.update_weather)
        self.timer_thread.start()
        # update the update interval submenu
        self.thread_lock.acquire()
        self.create_menu()
        self.thread_lock.release()


if __name__ == "__main__":
    # Ignore matplotlib Userwarning: The figure layout has been changed to tight. 
    warnings.filterwarnings("ignore", category=UserWarning)
    # Ignore: libpng warning: iCCP: known incorrect sRGB profile
    # I don't know how to ignore this warning. It's not a big deal.
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
    warnings.filterwarnings("default", category=UserWarning)

