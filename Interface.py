# Interface.py
# Description: GUI of the program
# By Monster Kid

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from WeatherAssistant import WeatherAssistant
from city_prediction import predict_city
from SerialPages import *

##########################################################################
# """
# GUI
# ------------------
# |Searchbox|   [City name]                        |[settings]
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
# [] Forecast weather, line chart
# [] Settings and multilanguage
# [] Icon and background color
# [] Min max temperature(currently not correct)
# [] Style and layout, font, color, etc. Window size, alignment, etc.
# [] Unblock the interface, use multithreading and add a loading animation
# [x] Error handling, when the city is not found, etc.
##########################################################################

class Interface(object):
    def __init__(self, master):

        self.weather_assistant = WeatherAssistant()
        # self.weather_assistant = WeatherAssistant(do_not_update=True)

        ## ----- Settings ----- ##
        self.settings = {
            "language": "English",
        }

        ## ----- Master ----- ##
        self.master = master
        self.master.title("Weather Assistant")
        self.master.geometry("1200x800")
        self.master.resizable(False, False)
        self.master.bind('<Button-1>', self.on_background_click)
        self.master.bind('<Return>', lambda event: self.add_city(self.city_entry.get()))
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        
        ## ----- Menu ----- ##
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        # City
        self.city_menu = tk.Menu(self.menu)
        self.city_menu.add_command(label="Remove City", command=None)
        self.menu.add_cascade(label="City", menu=self.city_menu)
        # Settings
        self.settings_menu = tk.Menu(self.menu)
        self.settings_menu.add_command(label="Language", command=None)
        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        # Help
        self.help_menu = tk.Menu(self.menu)
        self.help_menu.add_command(label="About", command=self.remove_city)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        ## ----- Background ----- ##
        # The background is a frame
        s = ttk.Style()
        s.configure("Background.TFrame", background="yellow")
        self.background_frame = ttk.Frame(master, style="Background.TFrame")
        self.background_frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
    
        # Configure columns and rows
        self.background_frame.rowconfigure(0, weight=1)
        self.background_frame.columnconfigure(0, weight=1)
        self.background_frame.columnconfigure(1, weight=10)
        
        ## ----- Left side ----- ##
        left_frame_style = ttk.Style()
        left_frame_style.configure("LeftFrame.TFrame", background="red")
        self.left_frame = ttk.Frame(self.background_frame, style="LeftFrame.TFrame")
        self.left_frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, weight=1)
        self.left_frame.rowconfigure(1, weight=10)
        # Search bar and City list on the left
        self.city_entry = tk.Entry(self.left_frame)
        self.city_entry.grid(row=0, column=0, sticky=tk.W+tk.E)
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

        ## ----- Right side ----- ##
        right_frame_style = ttk.Style()
        right_frame_style.configure("RightFrame.TFrame", background="blue")
        self.right_frame = ttk.Frame(self.background_frame, style="RightFrame.TFrame")
        self.right_frame.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W+tk.E)
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.rowconfigure(1, weight=1)
        self.right_frame.rowconfigure(2, weight=1)
        self.right_frame.rowconfigure(3, weight=1)
        self.right_frame.rowconfigure(4, weight=1)
        self.right_frame.rowconfigure(5, weight=10)
        self.right_frame.rowconfigure(6, weight=10)
        # City name and delete city button
        self.city_name_label = tk.Label(self.right_frame, text=self.weather_assistant.current_city)
        self.city_name_label.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        # Current Temperature
        # Style: Big font
        self.current_temperature_label = tk.Label(self.right_frame, text="0", font=("Helvetica", 48))
        self.current_temperature_label.grid(row=1, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        # Max / Min Temperature
        self.max_min_temperature_label = tk.Label(self.right_frame, text="0/0")
        self.max_min_temperature_label.grid(row=2, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        # Current Weather
        self.current_weather_label = tk.Label(self.right_frame, text="Weather")
        self.current_weather_label.grid(row=3, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        # Warning scrollbox
        self.warning_label = tk.Label(self.right_frame, text="Warning")
        self.warning_label.grid(row=4, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        # Weather scrollbox 
        self.weather_scrollbox = SerialDisplay(self.right_frame)
        self.now_weather_page = NowWeatherPage(self.weather_scrollbox)
        self.weather_scrollbox.add_page(self.now_weather_page)
        self.wind_page = WindPage(self.weather_scrollbox)
        self.weather_scrollbox.add_page(self.wind_page)
        self.index_page = IndexPage(self.weather_scrollbox)
        self.weather_scrollbox.add_page(self.index_page)
        self.weather_scrollbox.grid(row=5, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        # Chart scrollbox
        self.chart_scrollbox = SerialDisplay(self.right_frame)
        self.chart_24hours_page = Chart24HoursPage(self.chart_scrollbox)
        self.chart_7days_page = Chart7DaysPage(self.chart_scrollbox)
        self.chart_rain_page = ChartRainPage(self.chart_scrollbox)
        self.chart_scrollbox.add_page(self.chart_24hours_page)
        self.chart_scrollbox.add_page(self.chart_7days_page)
        self.chart_scrollbox.add_page(self.chart_rain_page)
        self.chart_scrollbox.grid(row=6, column=0, sticky=tk.N+tk.S+tk.W+tk.E)

        # Finalizing the layout
        self.master.focus()
        self.update()

    ## ----- Callback functions ----- ##

    def on_background_click(self, event):
        # When click on the background, the searchbox loses focus
        if event.widget != self.city_entry and event.widget != self.city_listbox:
            self.master.focus()

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
            city = self.city_listbox.get(self.city_listbox.curselection())
            self.add_city(city)
        else:
            # shift the selected city to the current city
            city = self.city_listbox.get(self.city_listbox.curselection())
            self.shift_city(city)

    ## ----- Functions ----- ##

    def add_city(self, city):
        res = self.weather_assistant.add_city(city)
        if res == "Success":
            self.update()
            messagebox.showinfo("Success", "City added")
            # clear the searchbox
            self.city_entry.delete(0, tk.END)
            # remove focus from searchbox
            self.master.focus()
        else: 
            messagebox.showerror("Error", res)

    def remove_city(self):
        res = self.weather_assistant.remove_city(self.weather_assistant.current_city)
        if res == "Success":
            self.update()
            messagebox.showinfo("Success", "City removed")
        else:
            messagebox.showerror("Error", res)

    def shift_city(self, city):
        city = self.city_listbox.get(self.city_listbox.curselection())
        res = self.weather_assistant.shift_city(city)
        if res == "Success":
            self.update()
        else:
            messagebox.showerror("Error", res)

    ## ----- Updating Functions ----- ##

    def update(self):
        self.update_weather()
        self.update_city_listbox()
        self.update_weather_scrollbox()
        self.update_chart_scrollbox()

    def update_weather(self):
        # Update current weather
        self.clear_all_labels()
        if self.weather_assistant.weather['now'] == None:
            return
        self.city_name_label.config(text=self.weather_assistant.current_city)
        self.current_temperature_label.config(text=str(int(self.weather_assistant.weather['now']['now']['temp'])) + "°C")
        self.max_min_temperature_label.config(text="###")
        self.current_weather_label.config(text=self.weather_assistant.weather['now']['now']['text'])
    
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
        if self.city_listbox_status == "predict_list":
            # delete all the items from the listbox
            self.city_listbox.delete(0, tk.END)
            # predict the city name
            text = self.city_entry.get()
            prediction_list = predict_city(text, self.weather_assistant.all_city_list, language=self.settings["language"])
            for city in prediction_list:
                self.city_listbox.insert(tk.END, city[2]["Name"])
        else:
            self.city_listbox.delete(0, tk.END)
            for city in self.weather_assistant.cities:
                self.city_listbox.insert(tk.END, city)

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()

