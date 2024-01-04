########### THIS IS THE ENTRY OF THE PROGRAM ###########
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
# Menu bar
# |Searchbox|   [City name]                         |
# |         |  [Temperture Number]                  |
# |City list|  [Max / Min Temperture]               |
# |         |  [Weather]                            |
# |         |  [Forecast Weather, line chart]       |
# |         |  [Update status]                      |
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
    """
    Graphical User Interface of the program
    Methods:
        __init__(self, master)          initialize the interface
        --- Callback functions ---
        on_background_click(self, event)
        on_master_return(self, event)
        searchbox_selected(self, event)
        searchbox_unselected(self, event)
        city_listbox_selected(self, event)
        city_listbox_unselected(self, event)
        city_listbox_click(self, event)
        --- Functions and Utilities ---
        save_settings(self)             save the settings to the settings file
        load_settings(self)             load the settings from the settings file
        create_menu(self)               create the menu bar
        add_city(self, city)            add a city to the city list
        remove_city(self)               remove the current city from the city list
        shift_city(self)                shift the selected city to the current city
        update_weather(self)            update the weather infomation
        handle_code(self, dict)         handle the error code returned by the API
        --- UI Updating Functions ---
        update_ui(self)                     update all the UI elements
        update_labels(self)                 update the labels on the right side
        update_warnings(self)               update the warning serial display
        update_weather_serial(self)         update the weather serial display
        undate_chart_serial(self)           update the chart serial display
        update_city_listbox(self, *args)    update the city listbox
        clear_all_labels(self)              clear all the labels on the right side
        --- Settings Functions ---
        change_language(self, language)         change the language of the program
        change_update_interval(self, interval)  change the update interval
    """

    ## ----- Constants ----- ##
    # The path of the settings file
    SETTING_PATH = "data/settings.json"
    # Default settings
    DEFAULT_SETTINGS = {
        "language": "English",
        "update_interval": 300, 
    }

    def __init__(self, master):

        ## ----- Settings ----- ##
        self.settings = self.load_settings()

        ## ----- Controller ----- ##
        self.weather_assistant = WeatherAssistant(language=language_alias_dict[self.settings["language"]])

        ## ----- Threads ----- ##
        # Thread lock to control access to the weather assistant and the UI
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
    
        # left-right ratio
        self.left_frame_ratio = 1 / 6
        self.right_frame_ratio = 1 - self.left_frame_ratio
        
        ## ----- Left side ----- ##
        # The left frame
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
        # City entry string variable to trace the change of the entry
        self.city_entry_var = tk.StringVar()
        self.city_entry_var.trace_add('write', self.update_city_listbox)
        self.city_entry.config(textvariable=self.city_entry_var)
        self.city_entry.bind('<FocusIn>', self.searchbox_selected)
        self.city_entry.bind('<FocusOut>', self.searchbox_unselected)
        # When there's text in searchbox, below the searchbox are prediction cities
        # The city listbox: display the city list or the prediction list when searchbox is selected
        self.city_listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE)
        self.city_listbox.bind('<Double-Button-1>', self.city_listbox_click)
        self.city_listbox.grid(row=1, column=0, rowspan=4, sticky=tk.N+tk.S+tk.W+tk.E)
        self.city_listbox_status = "city_list" # "city_list" or "predict_list"
        self.city_listbox.bind('<FocusIn>', self.city_listbox_selected)
        self.city_listbox.bind('<FocusOut>', self.city_listbox_unselected)
        # The prediction list
        self.prediction_list = []

        ## ----- Right side ----- ##
        # The right frame
        self.right_frame = ttk.Frame(self.background_frame)
        self.right_frame.place(relx=self.left_frame_ratio, rely=0, relwidth=self.right_frame_ratio, relheight=1)
        # PLACE all the widgets in the right frame
        # These ratios are used to control the height of each widget on the right side
        self.rf_weights = [1, 2, 1, 1, 1, 3, 8, 1]
        self.rf_ratios = [weight / sum(self.rf_weights) for weight in self.rf_weights]
        # City name label
        self.city_name_label = tk.Label(self.right_frame, text=self.weather_assistant.current_city)
        self.city_name_label.place(relx=0, rely=0, relwidth=1, relheight=self.rf_ratios[0])
        # Current Temperature label
        # Style: Big font
        self.current_temperature_label = tk.Label(self.right_frame, text="0", font=("Microsoft YaHei", 44))
        self.current_temperature_label.place(relx=0, rely=self.rf_ratios[0], relwidth=1, relheight=self.rf_ratios[1])
        # Max / Min Temperature label
        self.max_min_temperature_label = tk.Label(self.right_frame, text="0/0")
        self.max_min_temperature_label.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1], relwidth=1, relheight=self.rf_ratios[2])
        # Current Weather label
        self.current_weather_label = tk.Label(self.right_frame, text="Weather")
        self.current_weather_label.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1]+self.rf_ratios[2], relwidth=1, relheight=self.rf_ratios[3])
        # Warning serial display
        self.warning_serial = SerialDisplay(self.right_frame, language=self.settings["language"])
        self.warning_serial.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1]+self.rf_ratios[2]+self.rf_ratios[3], relwidth=1, relheight=self.rf_ratios[4])
        # Weather serial display
        self.weather_serial = SerialDisplay(self.right_frame)
        self.now_weather_page = NowWeatherPage(self.weather_serial, language=self.settings["language"])
        self.air_page = AirPage(self.weather_serial, language=self.settings["language"])
        self.index_page = IndexPage(self.weather_serial, language=self.settings["language"])
        self.sun_moon_page = SunMoonPage(self.weather_serial, language=self.settings["language"])
        self.wind_page = WindPage(self.weather_serial, language=self.settings["language"])
        self.weather_serial.add_page(self.now_weather_page)
        self.weather_serial.add_page(self.air_page)
        self.weather_serial.add_page(self.index_page)
        self.weather_serial.add_page(self.sun_moon_page)
        self.weather_serial.add_page(self.wind_page)
        self.weather_serial.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1]+self.rf_ratios[2]+self.rf_ratios[3]+self.rf_ratios[4], relwidth=1, relheight=self.rf_ratios[5])
        # Chart serial display
        self.chart_serial = SerialDisplay(self.right_frame, language=self.settings["language"])
        self.chart_24hours_page = Chart24HoursPage(self.chart_serial, language=self.settings["language"])
        self.chart_7days_page = Chart7DaysPage(self.chart_serial, language=self.settings["language"])
        self.chart_rain_page = ChartRainPage(self.chart_serial, language=self.settings["language"])
        self.chart_serial.add_page(self.chart_24hours_page)
        self.chart_serial.add_page(self.chart_7days_page)
        self.chart_serial.add_page(self.chart_rain_page)
        self.chart_serial.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1]+self.rf_ratios[2]+self.rf_ratios[3]+self.rf_ratios[4]+self.rf_ratios[5], relwidth=1, relheight=self.rf_ratios[6])
        # Last update time label
        self.last_update_time_label = tk.Label(self.right_frame, text=language_dict[self.settings["language"]]["last_update"])
        self.last_update_time_label.place(relx=0, rely=self.rf_ratios[0]+self.rf_ratios[1]+self.rf_ratios[2]+self.rf_ratios[3]+self.rf_ratios[4]+self.rf_ratios[5]+self.rf_ratios[6], relwidth=1, relheight=self.rf_ratios[7])

        # Finalizing the layout
        self.master.focus()
        self.master.update()
        self.update_ui()
        self.timer_thread.start()

    ## ----- Callback functions ----- ##

    def on_background_click(self, event):
        """
        When click on the background, the searchbox loses focus
        """
        if event.widget != self.city_entry and event.widget != self.city_listbox:
            self.master.focus()
    
    def on_master_return(self, event):
        """
        When press enter on the master, add the first city in the prediction list
        """
        if self.city_listbox_status == "predict_list":
            # add the selected city to the city list
            if not self.prediction_list:
                return
            self.add_city(self.prediction_list[0]["en"]["Name"])

    def searchbox_selected(self, event):
        """
        When the searchbox is selected, the city listbox displays the prediction list
        """
        self.city_listbox_status = "predict_list"
        self.update_city_listbox()

    def searchbox_unselected(self, event):
        """
        When the searchbox is unselected, the city listbox displays the city list
        But if the city listbox is selected, do nothing
        """
        # if listbox has focus, do nothing
        if self.master.focus_get() != self.city_listbox:
            self.city_listbox_status = "city_list"
            self.update_city_listbox()

    def city_listbox_selected(self, event):
        """
        Do nothing when the city listbox is selected
        """
        return
    
    def city_listbox_unselected(self, event):
        """
        When the city listbox is unselected, the city listbox displays the city list
        But if the searchbox is selected, do nothing
        """
        # if searchbox has focus, do nothing
        if self.master.focus_get() != self.city_entry:
            self.city_listbox_status = "city_list"
            self.update_city_listbox()
    
    def city_listbox_click(self, event):
        """
        When double click on the city listbox, add the selected city to the city list
        If the city listbox is predicting, add the first city in the prediction list
        """
        # If predicting, add the first city in the prediction list
        if self.city_listbox_status == "predict_list":
            # Check if the prediction list is empty
            if self.city_listbox.curselection() == ():
                return
            # add the selected city to the city list
            selected_city_idx = self.city_listbox.curselection()[0]
            selected_city = self.prediction_list[selected_city_idx]["en"]["Name"]
            self.add_city(selected_city)
        else:
            # shift the selected city to the current city
            self.shift_city()

    ## ----- Functions ----- ##

    def create_menu(self):
        """
        Create the menu bar
        """

        self.menu.delete(0, tk.END)
        # City Menu
        self.city_menu = tk.Menu(self.menu, tearoff=False)
        self.city_menu.add_command(label=language_dict[self.settings["language"]]["remove_city_command"], command=self.remove_city)
        self.city_menu.add_command(label=language_dict[self.settings["language"]]["update_weather_command"], command=self.update_weather)
        self.menu.add_cascade(label=language_dict[self.settings["language"]]["city_menu"], menu=self.city_menu)
        # Settings Menu
        self.settings_menu = tk.Menu(self.menu, tearoff=False)
        # Language submenu
        self.language_submenu = tk.Menu(self.settings_menu, tearoff=False)
        self.language_submenu.add_command(label=language_dict[self.settings["language"]]["english_command"], command=lambda: self.change_language("English"))
        self.language_submenu.add_command(label=language_dict[self.settings["language"]]["chinese_command"], command=lambda: self.change_language("Chinese"))
        # Update interval submenu
        self.update_interval_submenu = tk.Menu(self.settings_menu, tearoff=False)
        self.update_interval_submenu.add_command(label=language_dict[self.settings["language"]]["10_seconds"], command=lambda: self.change_update_interval(10))
        self.update_interval_submenu.add_command(label=language_dict[self.settings["language"]]["5_minutes"], command=lambda: self.change_update_interval(300))
        self.update_interval_submenu.add_command(label=language_dict[self.settings["language"]]["10_minutes"], command=lambda: self.change_update_interval(600))
        self.update_interval_submenu.add_command(label=language_dict[self.settings["language"]]["30_minutes"], command=lambda: self.change_update_interval(1800))
        self.update_interval_submenu.add_command(label=language_dict[self.settings["language"]]["1_hour"], command=lambda: self.change_update_interval(3600))
        # Add submenus to the settings menu
        self.menu.add_cascade(label=language_dict[self.settings["language"]]["settings_menu"], menu=self.settings_menu)
        self.settings_menu.add_cascade(label=language_dict[self.settings["language"]]["language_menu"], menu=self.language_submenu, underline=0)
        # update interval submenu text: display the current update interval
        text_update_interval = language_dict[self.settings["language"]]["update_interval"] + ": " + \
                                 language_dict[self.settings["language"]][sec2natural_dict[self.settings["update_interval"]]]
        self.settings_menu.add_cascade(label=text_update_interval, menu=self.update_interval_submenu, underline=0)
        # Help Menu
        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.help_menu.add_command(label=language_dict[self.settings["language"]]["help_menu"], command=lambda: messagebox.showinfo("About us", "Weather Assistant\nBy Monster Kid\nSupport: Hefeng Weather"))
        self.menu.add_cascade(label=language_dict[self.settings["language"]]["help_menu"], menu=self.help_menu)
    
    def save_settings(self):
        """
        Save the settings to the settings file
        """
        with open(self.SETTING_PATH, 'w') as f:
            json.dump(self.settings, f)
    
    def load_settings(self):
        """
        Load the settings from the settings file
        """
        if not os.path.exists(self.SETTING_PATH):
            return self.DEFAULT_SETTINGS
        with open(self.SETTING_PATH, 'r') as f:
            return json.load(f)
    
    def add_city(self, city):
        """
        Add a city to the city list
        """
        # Use a thread to add the city
        thread = threading.Thread(target=self.add_city_thread, args=(city,))
        thread.start()

    def add_city_thread(self, city=None):
        """
        Thread: Add a city to the city list
        """

        # It's accessing the weather assistant and the UI, so it must acquire the lock
        self.thread_lock.acquire()
        self.last_update_time_label.config(text=language_dict[self.settings["language"]]["updating"])
        # Add the city in the weather assistant
        res = self.weather_assistant.add_city(city)
        # Message box and update the UI
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
        
        # Release the lock
        self.thread_lock.release()
    
    def remove_city(self):
        """
        Remove the current city from the city list
        """
        
        thread = threading.Thread(target=self.remove_city_thread)
        thread.start()

    def remove_city_thread(self):
        """
        Thread: Remove the current city from the city list
        """

        # I don't write the comments, please refer to the add_city_thread function
        self.thread_lock.acquire()
        self.last_update_time_label.config(text=language_dict[self.settings["language"]]["updating"])
        res = self.weather_assistant.remove_city(self.weather_assistant.current_city)
        if res == "success":
            self.update_ui()
            messagebox.showinfo(language_dict[self.settings["language"]]["success"], \
                                language_dict[self.settings["language"]]["city_removed"])
        else:
            messagebox.showerror(language_dict[self.settings["language"]]["error"], \
                                language_dict[self.settings["language"]][res])
        self.thread_lock.release()
    
    def shift_city(self):
        """
        Shift the selected city to the current city
        """

        # check if the curselecion is empty
        if self.city_listbox.curselection() == ():
            return
        city_idx = self.city_listbox.curselection()[0]
        city = list(self.weather_assistant.cities)[city_idx]
        thread = threading.Thread(target=self.shift_city_thread, args=(city,))
        thread.start()

    def shift_city_thread(self, city):
        """
        Thread: Shift the selected city to the current city
        """

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
        """
        Update the weather infomation
        """

        thread = threading.Thread(target=self.update_weather_thread)
        thread.start()
        
    def update_weather_thread(self):
        """
        Thread: Update the weather infomation
        """

        self.thread_lock.acquire()
        self.last_update_time_label.config(text=language_dict[self.settings["language"]]["updating"])
        self.weather_assistant.update_weather()
        self.update_ui()
        self.thread_lock.release()
    
    def handle_code(self, dict: dict) -> tuple:
        """
        Handle the error code returned by the API
        :param dict: the dictionary returned by the API
        :return: the code and the error message, 
                    the error message are keys in the language_dict
        """
        
        # Check if the dict is None
        if dict == None:
            return "0", "dict_is_none"
        code = dict["code"]
        # err dict: map the code to the error message
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
        """
        Update all the UI elements
        """
        self.update_labels()
        self.update_city_listbox()
        self.update_weather_serial()
        self.undate_chart_serial()
        self.update_warnings()

    def update_labels(self):
        """
        Update the labels on the right side
        """

        # Update current weather
        self.clear_all_labels()
        # If there's no current city, display "No city"
        if self.weather_assistant.current_city == None:
            self.city_name_label.config(text=language_dict[self.settings["language"]]["no_city"])
            return
        self.city_name_label.config(text=self.weather_assistant.all_cities[self.weather_assistant.current_city][language_alias_dict[self.settings["language"]]]["Name"])

        # Update current weather
        code, err = self.handle_code(self.weather_assistant.weather['now'])
        if code != "200":
            # If error, display the error message
            self.current_temperature_label.config(text=language_dict[self.settings["language"]][err])
            # self.current_weather_label.config(text=language_dict[self.settings["language"]]["update_failure"])
            # self.last_update_time_label.config(text=language_dict[self.settings["language"]]["update_failure"])
        else:
            # If success, display the current weather
            self.current_temperature_label.config(text=str(int(self.weather_assistant.weather['now']['now']['temp'])) + "°C")
            self.current_weather_label.config(text=self.weather_assistant.weather['now']['now']['text'])
            # datetime string is ISO 8601 format
            parsed_time = time.strptime(self.weather_assistant.weather['now']['updateTime'], "%Y-%m-%dT%H:%M%z")
            text = language_dict[self.settings["language"]]["last_update"] + time.strftime("%Y-%m-%d %H:%M", parsed_time)
            text += " " + self.weather_assistant.weather['now']['refer']['sources'][0]
            text += " " + self.weather_assistant.weather['now']['refer']['license'][0]
            self.last_update_time_label.config(text=text)

        # Update max min temperature
        code, err = self.handle_code(self.weather_assistant.weather['7d'])
        if code != "200":
            pass
        else:
            self.max_min_temperature_label.config(text=str(int(self.weather_assistant.weather['7d']['daily'][0]['tempMin'])) + "°C / " + str(int(self.weather_assistant.weather['7d']['daily'][0]['tempMax'])) + "°C")
    
    def update_warnings(self):
        """
        Update the warning serial display
        """

        # Clear all the pages
        self.warning_serial.delete_all_pages()

        # Check the code
        code, err = self.handle_code(self.weather_assistant.weather['warning'])
        if code != "200" or self.weather_assistant.weather['warning']['warning'] == None:
            # If error, display the error message
            error_page = WarningPage(self.warning_serial, language_dict[self.settings["language"]][err])
            self.warning_serial.add_page(error_page)
            return

        # If success, display the warnings. Add a page for each warning
        data = self.weather_assistant.weather['warning']['warning']
        if len(data) == 0:
            no_warning_page = WarningPage(self.warning_serial, language_dict[self.settings["language"]]["no_warning"])
            self.warning_serial.add_page(no_warning_page)
        else:
            for warning in data:
                warning_page = WarningPage(self.warning_serial, warning["title"])
                self.warning_serial.add_page(warning_page) 
    
    def update_weather_serial(self):
        """
        Update the weather serial display
        """

        # Clear all the pages
        self.weather_serial.clear()
        # Check if there's a current city
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
    
    def undate_chart_serial(self):
        """
        Update the chart serial display
        """

        # Clear all the pages
        self.chart_serial.clear()
        # Check if there's a current city
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
        """
        Clear all the labels on the right side
        """

        self.city_name_label.config(text="")
        self.current_temperature_label.config(text="")
        self.max_min_temperature_label.config(text="")
        self.current_weather_label.config(text="")
        self.last_update_time_label.config(text="")
    
    def update_city_listbox(self, *args):
        """
        Update the city listbox
        """

        self.prediction_list = []
        if self.city_listbox_status == "predict_list":
            # delete all the items from the listbox
            self.city_listbox.delete(0, tk.END)
            # predict the city name
            text = self.city_entry.get()
            self.prediction_list = predict_city(text, self.weather_assistant.all_cities, language=self.settings["language"])
            # add the prediction list to the listbox
            for city in self.prediction_list:
                display = city[language_alias_dict[self.settings["language"]]]["Name"]
                state = city[language_alias_dict[self.settings["language"]]]["StateName"] if city['type'] == 'city' else None
                country = city[language_alias_dict[self.settings["language"]]]["CountryName"]
                display += ", " + state if state is not None and state != "None" else ""
                self.city_listbox.insert(tk.END, display)
        else:
            # display the city list
            self.city_listbox.delete(0, tk.END)
            for city in self.weather_assistant.cities:
                display = self.weather_assistant.all_cities[city][language_alias_dict[self.settings["language"]]]["Name"]
                self.city_listbox.insert(tk.END, display)
    
    ## ----- Settings Functions ----- ##

    def change_language(self, language):
        """
        Change the language of the program
        """

        # change the language in the settings
        self.settings["language"] = language
        self.save_settings()

        # change the title and the menu
        self.master.title(language_dict[self.settings["language"]]["title"])
        self.create_menu()
        
        self.thread_lock.acquire()
        # change the language in the weather assistant
        self.weather_assistant.set_language(language_alias_dict[self.settings["language"]])
        # change the language in the serial displays
        self.weather_serial.set_language(self.settings["language"])
        self.warning_serial.set_language(self.settings["language"])
        self.chart_serial.set_language(self.settings["language"])
        # update the UI
        self.update_ui()
        self.thread_lock.release()
    
    def change_update_interval(self, interval):
        """
        Change the update interval
        """

        # change the update interval in the settings
        self.settings["update_interval"] = interval
        self.save_settings()
        # kill the timer thread and restart it
        self.timer_thread.stop()
        self.timer_thread = TimerThread(self.settings["update_interval"], self.update_weather)
        self.timer_thread.start()
        # update the update interval submenu
        # this is a dirty way to do this
        self.thread_lock.acquire()
        self.create_menu()
        self.thread_lock.release()


# Entry of the program
if __name__ == "__main__":
    # Ignore matplotlib Userwarning: The figure layout has been changed to tight. 
    warnings.filterwarnings("ignore", category=UserWarning)
    # Ignore: libpng warning: iCCP: known incorrect sRGB profile
    # I don't know how to ignore this warning. It's not a big deal.
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
    warnings.filterwarnings("default", category=UserWarning)

