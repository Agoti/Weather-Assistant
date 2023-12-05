# Interface.py
# Description: GUI of the program
# By Monster Kid

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from WeatherAssistant import WeatherAssistant
from city_prediction import predict_city

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
# [] Version control, git
# [] Forecast weather, line chart
# [] Settings and multilanguage
# [] Icon and background color
# [] Min max temperature(currently not correct)
# [] Style and layout, font, color, etc. Window size, alignment, etc.
# [] Unblock the interface, use multithreading and add a loading animation
# [] Error handling, when the city is not found, etc.
##########################################################################

class Interface(object):
    def __init__(self, master):

        ## ----- Master ----- ##
        self.master = master
        self.master.title("Weather Assistant")
        self.master.geometry("400x300")
        self.master.resizable(False, False)
        
        self.weather_assistant = WeatherAssistant()

        ## ----- Background ----- ##
        # The background is a frame
        self.background_frame = tk.Frame(master)
        self.background_frame.bind('<Button-1>', self.on_background_click)
        
        ## ----- Settings ----- ##
        self.settings = {
            "language": "English",
        }

        ## ----- Left side ----- ##
        # Search bar and City list on the left
        self.city_entry = tk.Entry(self.background_frame)
        self.city_entry.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        # The add city button is used for testing, 
        # it will be removed after the prediction function is implemented
        # self.add_city_button = tk.Button(master, text="Add City", command=self.add_city)
        # self.add_city_button.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W+tk.E)
        # When the searchbox is selected, the city list is disabled
        self.city_entry_var = tk.StringVar()
        self.city_entry_var.trace('w', self.update_city_listbox)
        self.city_entry.config(textvariable=self.city_entry_var)
        self.city_entry.bind('<FocusIn>', self.searchbox_selected)
        self.city_entry.bind('<FocusOut>', self.searchbox_unselected)
        # When there's text in searchbox, below the searchbox are prediction cities
        # TODO: prediction function
        # The city listbox
        self.city_listbox = tk.Listbox(self.background_frame, selectmode=tk.SINGLE)
        self.city_listbox.bind('<Double-Button-1>', self.city_listbox_click)
        self.city_listbox.grid(row=1, column=0, rowspan=4, sticky=tk.N+tk.S+tk.W+tk.E)
        self.city_listbox_status = "city_list"
        self.city_listbox.bind('<FocusIn>', self.city_listbox_selected)
        self.city_listbox.bind('<FocusOut>', self.city_listbox_unselected)

        ## ----- Right side ----- ##
        # City name and delete city button
        self.city_name_label = tk.Label(self.background_frame, text=self.weather_assistant.current_city)
        self.city_name_label.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W+tk.E)
        self.remove_city_button = ttk.Button(self.background_frame, text="Remove City", command=self.remove_city)
        self.remove_city_button.grid(row=0, column=2, sticky=tk.N+tk.S+tk.W+tk.E) 
        # Current Temperature
        # Style: Big font
        self.current_temperature_label = tk.Label(self.background_frame, text="0", font=("Helvetica", 48))
        self.current_temperature_label.grid(row=1, column=1, sticky=tk.N+tk.S+tk.W+tk.E)
        # Max / Min Temperature
        self.max_min_temperature_label = tk.Label(self.background_frame, text="0/0")
        self.max_min_temperature_label.grid(row=2, column=1, sticky=tk.N+tk.S+tk.W+tk.E)
        # Current Weather
        self.current_weather_label = tk.Label(self.background_frame, text="Weather")
        self.current_weather_label.grid(row=3, column=1, sticky=tk.N+tk.S+tk.W+tk.E)
        # Humidity | Wind | Pressure | Clouds
        self.humidity_wind_pressure_clouds_label = tk.Label(self.background_frame, text="0% | 0m/s | 0hPa | 0%")
        self.humidity_wind_pressure_clouds_label.grid(row=4, column=1, sticky=tk.N+tk.S+tk.W+tk.E)

        # Finalizing the layout
        self.background_frame.pack()
        self.update_weather()

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
        if city:
            self.weather_assistant.add_city(city)
            messagebox.showinfo("Success", f"{city} added to the city list.")
        else:
            messagebox.showwarning("Warning", "Please enter a city name.")
        self.update_weather()

    def remove_city(self):
        self.weather_assistant.remove_city(self.weather_assistant.current_city)
        self.update_weather()

    def shift_city(self, city):
        city = self.city_listbox.get(self.city_listbox.curselection())
        self.weather_assistant.shift_city(city)
        self.update_weather()

    ## ----- Updating Functions ----- ##

    def update_weather(self):
        # Update city list
        self.city_listbox.delete(0, tk.END)
        for city in self.weather_assistant.cities:
            self.city_listbox.insert(tk.END, city)
        # Update current weather
        self.city_name_label.config(text=self.weather_assistant.current_city)
        self.current_temperature_label.config(text=str(int(self.weather_assistant.current_weather[2]['main']['temp'] - 273.15)))
        self.max_min_temperature_label.config(text=str(int(self.weather_assistant.current_weather[2]['main']['temp_max'] - 273.15)) + "/" + str(int(self.weather_assistant.current_weather[2]['main']['temp_min'] - 273.15)))
        self.current_weather_label.config(text=self.weather_assistant.current_weather[2]['weather']['main'])
        self.humidity_wind_pressure_clouds_label.config(text=str(int(self.weather_assistant.current_weather[2]['main']['humidity'])) + "% | " + str(int(self.weather_assistant.current_weather[2]['wind']['speed'])) + "m/s | " + str(int(self.weather_assistant.current_weather[2]['main']['pressure'])) + "hPa | " + str(int(self.weather_assistant.current_weather[2]['clouds'])) + "%")
    
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

