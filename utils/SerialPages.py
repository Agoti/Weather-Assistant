import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from assets.multi_lang_dict import *
import matplotlib.pyplot as plt
import numpy as np

# Matplotlib Chinese support
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Abstract class
class SerialPage(tk.Frame):
    OCC = "---"
    def __init__(self, parent, language = "English"):
        super().__init__(parent)
        self.parent = parent
        self.language = language
    
    def update(self, **kwargs):
        pass
        
    def clear(self):
        pass

    def set_language(self, language):
        pass

class NowWeatherPage(SerialPage):
    def __init__(self, parent, language = "English"):
        super().__init__(parent, language)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.title = language_dict[self.language]['now_weather_title']
        self.keys = ['humidity', 'feelsLike', 'windDir', 'windScale', 'pressure', 'vis', 'cloud']
        self.subtitle = language_dict[self.language]['now_weather_subtitle']
        self.units = language_dict[self.language]['now_weather_units']
        self.title_label = tk.Label(self, text=self.title)
        self.title_label.grid(row=0, column=0, columnspan=len(self.keys), padx=10, pady=10)

        for i, key in enumerate(self.keys):
            self.columnconfigure(i, weight=1)

            label = tk.Label(self, text=self.subtitle[i])
            label.grid(row=1, column=i, padx=10, pady=10)
            setattr(self, f"{key}_label", label)

            value_label = tk.Label(self, text=self.OCC)
            value_label.grid(row=2, column=i, padx=10, pady=10)
            setattr(self, key, value_label)

    
    def update(self, **kwargs):
        self.clear()
        for i, key in enumerate(self.keys):
            getattr(self, key)['text'] = kwargs[key] + self.units[i]

    def clear(self):
        for key in self.keys:
            getattr(self, key)['text'] = self.OCC
    
    def set_language(self, language):
        self.language = language
        self.title = language_dict[self.language]['now_weather_title']
        self.subtitle = language_dict[self.language]['now_weather_subtitle']
        self.units = language_dict[self.language]['now_weather_units']
        self.title_label['text'] = self.title
        for i, key in enumerate(self.keys):
            getattr(self, key + '_label')['text'] = self.subtitle[i]
            getattr(self, key)['text'] = self.OCC

class AirPage(SerialPage):
    def __init__(self, parent, language = "English"):
        super().__init__(parent, language)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.title = language_dict[self.language]['air_quality_title']
        self.keys = ['aqi', 'category', 'primary', 'pm10', 'pm2p5', 'no2', 'so2', 'co', 'o3']
        self.subtitle = language_dict[self.language]['air_quality_subtitle']
        self.units = language_dict[self.language]['air_quality_units']
        self.title_label = tk.Label(self, text=self.title)
        self.title_label.grid(row=0, column=0, columnspan=len(self.keys), padx=10, pady=10)
        for i, key in enumerate(self.keys):
            self.columnconfigure(i, weight=1)

            label = tk.Label(self, text=self.subtitle[i])
            label.grid(row=1, column=i, padx=10, pady=10)
            setattr(self, f"{key}_label", label)

            value_label = tk.Label(self, text=self.OCC)
            value_label.grid(row=2, column=i, padx=10, pady=10)
            setattr(self, key, value_label)
    
    def update(self, **kwargs):
        self.clear()
        for i, key in enumerate(self.keys):
            getattr(self, key)['text'] = kwargs[key] + self.units[i]
    
    def clear(self):
        for key in self.keys:
            getattr(self, key)['text'] = self.OCC
    
    def set_language(self, language):
        self.language = language
        self.title = language_dict[self.language]['air_quality_title']
        self.subtitle = language_dict[self.language]['air_quality_subtitle']
        self.units = language_dict[self.language]['air_quality_units']
        self.title_label['text'] = self.title
        for i, key in enumerate(self.keys):
            getattr(self, key + '_label')['text'] = self.subtitle[i]
            getattr(self, key)['text'] = self.OCC


class WindPage(SerialPage):
    def __init__(self, parent, language = "English"):
        super().__init__(parent, language)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.title = language_dict[self.language]['wind_title']
        self.keys = ['windDir', 'windScale', 'windSpeed', 'wind360']
        self.subtitle = language_dict[self.language]['wind_subtitle']
        self.units = language_dict[self.language]['wind_units']
        self.title_label = tk.Label(self, text=self.title)
        self.title_label.grid(row=0, column=0, columnspan=len(self.keys), padx=10, pady=10)
        for i, key in enumerate(self.keys):
            self.columnconfigure(i, weight=1)

            label = tk.Label(self, text=self.subtitle[i])
            label.grid(row=1, column=i, padx=10, pady=10)
            setattr(self, f"{key}_label", label)

            value_label = tk.Label(self, text=self.OCC)
            value_label.grid(row=2, column=i, padx=10, pady=10)
            setattr(self, key, value_label)

    def update(self, **kwargs):
        self.clear()
        for i, key in enumerate(self.keys):
            getattr(self, key)['text'] = kwargs[key] + self.units[i]
        
    def clear(self):
        for key in self.keys:
            getattr(self, key)['text'] = self.OCC
    
    def set_language(self, language):
        self.language = language
        self.title = language_dict[self.language]['wind_title']
        self.subtitle = language_dict[self.language]['wind_subtitle']
        self.units = language_dict[self.language]['wind_units']
        self.title_label['text'] = self.title
        for i, key in enumerate(self.keys):
            getattr(self, key + '_label')['text'] = self.subtitle[i]
            getattr(self, key)['text'] = self.OCC
    
    # def get_direction(self, direction360):
    #     dir_main = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    #     dir_idx = int((direction360 + 22.5) / 45)
    #     dir_remainder = (direction360 + 22.5) % 45
    #     return language_dict[self.language]['wind_direction'][dir_main[dir_idx % 8]] +\


class SunMoonPage(SerialPage):
    def __init__(self, parent, language = "English"):
        super().__init__(parent, language)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.title = language_dict[self.language]['sun_moon_title']
        self.keys = ['sunrise', 'sunset', 'moonrise', 'moonset', 'moonPhase']
        self.subtitle = language_dict[self.language]['sun_moon_subtitle']
        self.units = language_dict[self.language]['sun_moon_units']
        self.title_label = tk.Label(self, text=self.title)
        self.title_label.grid(row=0, column=0, columnspan=len(self.keys), padx=10, pady=10)
        for i, key in enumerate(self.keys):
            self.columnconfigure(i, weight=1)

            label = tk.Label(self, text=self.subtitle[i])
            label.grid(row=1, column=i, padx=10, pady=10)
            setattr(self, f"{key}_label", label)

            value_label = tk.Label(self, text=self.OCC)
            value_label.grid(row=2, column=i, padx=10, pady=10)
            setattr(self, key, value_label)
    
    def update(self, **kwargs):
        self.clear()
        for i, key in enumerate(self.keys):
            getattr(self, key)['text'] = kwargs[key] + self.units[i]
    
    def clear(self):
        for key in self.keys:
            getattr(self, key)['text'] = self.OCC
    
    def set_language(self, language):
        self.language = language
        self.title = language_dict[self.language]['sun_moon_title']
        self.subtitle = language_dict[self.language]['sun_moon_subtitle']
        self.units = language_dict[self.language]['sun_moon_units']
        self.title_label['text'] = self.title
        for i, key in enumerate(self.keys):
            getattr(self, key + '_label')['text'] = self.subtitle[i]
            getattr(self, key)['text'] = self.OCC
        

class IndexPage(SerialPage):
    def __init__(self, parent, language = "English"):
        super().__init__(parent, language)
        self.scroll_canvas = tk.Canvas(self)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scrollbar = tk.Scrollbar(self, command=self.scroll_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)

    def update(self, **kwargs):
        self.clear()
        # if no arguments, add a default label
        if len(kwargs) == 0:
            label = tk.Label(self.scroll_canvas, text=language_dict[self.language]['no_content'])
            self.scroll_canvas.create_window((0, 0), window=label, anchor=tk.NW)
            return
        today = kwargs['daily'][0]['date']
        cnt = 0
        for i in range(len(kwargs['daily'])):
            if kwargs['daily'][i]['date'] == today:
                label_text = f"{kwargs['daily'][i]['name']}: {kwargs['daily'][i]['category']}"
                label = tk.Label(self.scroll_canvas, text=label_text)
                # 2 labels per row
                self.scroll_canvas.create_window((cnt % 2 * 300, cnt // 2 * 20), window=label, anchor=tk.NW)
                cnt += 1

        # Update the scroll region based on the content size
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))

    def clear(self):
        self.scroll_canvas.delete("all")
    
    def set_language(self, language):
        self.language = language


class Chart7DaysPage(SerialPage):
    def __init__(self, parent, language = "English"):
        super().__init__(parent, language)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.title = language_dict[self.language]['7d_title']

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update(self, **kwargs):
        self.clear()
        # data is a list of dict
        data = kwargs['daily']
        x = np.arange(len(data))
        y1 = [int(data[i]['tempMax']) for i in range(len(data))]
        self.ax.plot(x, y1)
        y2 = [int(data[i]['tempMin']) for i in range(len(data))]
        self.ax.plot(x, y2)
        self.ax.scatter(x, y1)
        self.ax.scatter(x, y2)
        y1_span = max(y1) - min(y2)
        for i in range(len(data)):
            y_offset_1 = 10 if y1_span and (y1[i] - min(y2)) / y1_span < 0.8 else -20
            y_offset_2 = 10
            self.ax.annotate(str(y1[i]) + "°C", (x[i], y1[i]), textcoords="offset points", xytext=(0, y_offset_1),
                             ha='center')
            self.ax.annotate(str(y2[i]) + "°C", (x[i], y2[i]), textcoords="offset points", xytext=(0, y_offset_2),
                             ha='center')

        # 设置横轴刻度标签
        x_labels = [data[i]['fxDate'][5:] for i in range(len(data))]
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(x_labels)

        self.canvas.draw()
    
    def clear(self):
        self.ax.clear()
        self.ax.set_title(self.title)
        self.ax.set_yticks([])
        self.canvas.draw()
    
    def set_language(self, language):
        self.language = language
        self.title = language_dict[self.language]['7d_title']
        self.ax.set_title(self.title)


class Chart24HoursPage(SerialPage):
    def __init__(self, parent, language = "English"):
        super().__init__(parent, language)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.title = language_dict[self.language]['24h_title']

        # Create a canvas and a scrollbar,
        # then embed Frame-FigureCanvasTkAgg in the canvas
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Create a Frame
        self.frame = tk.Frame(self.canvas)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        # Adjust figure size to fit the frame
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def update_size(self, *args):
        # Make the frame fill the whole canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        # Avoid scroll bar
        canvas_height = max(1, canvas_height - 20)
        self.frame.config(width=canvas_width * 3, height=canvas_height)
        self.fig_canvas.get_tk_widget().config(width=canvas_width * 3, height=canvas_height)
        self.fig_canvas.draw()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    def update(self, **kwargs):
        self.clear()
        self.update_size()
        self.ax.set_yticks([])
        # data is a list of dict
        data = kwargs['hourly']
        x = np.arange(len(data))
        y1 = [int(data[i]['temp']) for i in range(len(data))]
        self.ax.plot(x, y1, color='red')
        self.ax.scatter(x, y1, color='red')
        span = max(y1) - min(y1)
        for i in range(len(data)):
            y_offset = 10 if span and (y1[i] - min(y1)) / span < 0.8 else -20
            self.ax.annotate(str(y1[i]) + "°C", (x[i], y1[i]), textcoords="offset points", xytext=(0, y_offset),
                             ha='center', color='red')
        x_labels = [data[i]['fxTime'][11:16] for i in range(len(data))]
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(x_labels)  # Rotate x-axis labels for better visibility
        self.fig.tight_layout()
        self.fig.subplots_adjust(bottom=0.2, top=0.8)
        self.fig_canvas.draw()

    def clear(self):
        self.update_size()
        self.ax.clear()
        self.ax.set_title(self.title)
        self.ax.set_yticks([])
        self.fig_canvas.draw()
    
    def set_language(self, language):
        self.language = language
        self.title = language_dict[self.language]['24h_title']
        self.ax.set_title(self.title)


class ChartRainPage(SerialPage):
    def __init__(self, parent, language = "English"):
        super().__init__(parent, language)
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        # self.title = language_dict[self.language]['rain_title']
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    def update(self, **kwargs):
        self.clear()
        # data is a list of dict
        data = kwargs['minutely']
        x = np.arange(len(data))
        y1 = [float(data[i]['precip']) for i in range(len(data))]
        # self.ax.scatter(x, y1)
        self.ax.plot(x, y1)

        span = max(y1) - min(y1)
        for i in range(len(data)):
            y_offset = 10 if span and (y1[i] - min(y1)) / span < 0.9 else -20
            if y1[i] > 0:
                self.ax.annotate(str(y1[i]), (x[i], y1[i]), textcoords="offset points", xytext=(0, y_offset), ha='center')

        self.ax.set_ylim(-0.1, max(max(y1), 1) * 1.1)
        self.ax.set_yticks([])

        x_labels = [data[i]['fxTime'][11:16] for i in range(len(data))]
        self.ax.set_xticks(x[::6])
        self.ax.set_xticklabels(x_labels[::6])

        title = kwargs['summary']
        self.ax.set_title(title)

        self.canvas.draw()
    
    def clear(self):
        self.ax.clear()
        self.ax.set_title("")
        self.ax.set_yticks([])
        self.canvas.draw()
    
    def set_language(self, language):
        self.language = language
        # self.title = language_dict[self.language]['rain_title']
        # self.ax.set_title(self.title)

class WarningPage(SerialPage):
    def __init__(self, parent, text, language = "English"):
        super().__init__(parent, language)
        self.text_label = tk.Label(self, text=text)
        self.text_label.pack()
    
    def update(self, **kwargs):
        pass
    
    def clear(self):
        pass

    def set_language(self, language):
        pass


class SerialDisplay(tk.Frame):
    def __init__(self, parent, language = "English"):
        super().__init__(parent)
        self.language = language
        self.current_page = 0
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=100)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)

        # 创建左右换页按钮
        self.prev_button = tk.Button(self, text="<", command=self.show_previous_page)
        self.prev_button.grid(row=0, column=0, sticky=tk.W)

        # 创建窗口
        self.serial_pages = []

        self.next_button = tk.Button(self, text=">", command=self.show_next_page)
        self.next_button.grid(row=0, column=2, sticky=tk.E)

        # 窗口前页
        self.show_current_page()
        
    def add_page(self, page):
        self.serial_pages.append(page)
        self.show_current_page()

    def show_current_page(self):
        for page in self.serial_pages:
            page.grid_forget()

        # 显示当前页
        if len(self.serial_pages) > 0:
            self.serial_pages[self.current_page].grid(row=0, column=1, sticky=tk.NSEW)
        
        self.update_button_state()

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()
        self.update_button_state()

    def show_next_page(self):
        if self.current_page < len(self.serial_pages) - 1:
            self.current_page += 1
            self.show_current_page()
        self.update_button_state()
    
    def update_button_state(self):
        if self.current_page == 0:
            self.prev_button['state'] = tk.DISABLED
        else:
            self.prev_button['state'] = tk.NORMAL
        if self.current_page == len(self.serial_pages) - 1:
            self.next_button['state'] = tk.DISABLED
        else:
            self.next_button['state'] = tk.NORMAL
    
    def clear(self):
        for page in self.serial_pages:
            page.clear()
    
    def delete_all_pages(self):
        # Delete all pages in serial_pages
        self.serial_pages = []
        self.current_page = 0
        self.show_current_page()
    
    def set_language(self, language):
        self.language = language
        for page in self.serial_pages:
            page.set_language(language)
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Serial Display")

    serial_display = SerialDisplay(root)
    weather_page = NowWeatherPage(serial_display)
    serial_display.add_page(weather_page)
    wind_page = WindPage(serial_display)
    serial_display.add_page(wind_page)
    index_page = IndexPage(serial_display)
    serial_display.add_page(index_page)
    chart_7days_page = Chart7DaysPage(serial_display)
    serial_display.add_page(chart_7days_page)
    # spawn random data to test chart
    tempdata = []
    for i in range(7):
        tempdata.append({
            'date': '2020-01-01',
            'tempMax': np.random.randint(0, 100),
            'tempMin': np.random.randint(0, 100),
            'name': 'test',
            'category': 'test'
        })
    chart_7days_page.update(daily=tempdata)
    serial_display.pack(padx=20, pady=20)
    temp24data = []
    for i in range(24):
        temp24data.append({
            'temp': np.random.randint(0, 100)
        })
    chart_24hours_page = Chart24HoursPage(serial_display)
    serial_display.add_page(chart_24hours_page)
    chart_24hours_page.update(hourly=temp24data)
    tempRaindata = []
    for i in range(24):
        tempRaindata.append({
            'precip': np.random.randint(0, 100)
        })
    chart_rain_page = ChartRainPage(serial_display)
    serial_display.add_page(chart_rain_page)
    chart_rain_page.update(minutely=tempRaindata)
    

    root.mainloop()
