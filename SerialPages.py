import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

# Matplotlib Chinese support
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Abstract class
class SerialPage(tk.Frame):
    OCC = "###"
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    def update(self, **kwargs):
        pass
        
    def clear(self):
        pass

class NowWeatherPage(SerialPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.humidity = tk.Label(self, text=self.OCC)
        self.humidity.grid(row=0, column=0, padx=10, pady=10)
        self.wind_direction = tk.Label(self, text=self.OCC)
        self.wind_direction.grid(row=0, column=1, padx=10, pady=10)
        self.wind_speed = tk.Label(self, text=self.OCC)
        self.wind_speed.grid(row=0, column=2, padx=10, pady=10)
        self.pressure = tk.Label(self, text=self.OCC)
        self.pressure.grid(row=1, column=0, padx=10, pady=10)
        self.visibility = tk.Label(self, text=self.OCC)
        self.visibility.grid(row=1, column=1, padx=10, pady=10)
        self.cloud = tk.Label(self, text=self.OCC)
        self.cloud.grid(row=1, column=2, padx=10, pady=10)
    
    def update(self, **kwargs):
        self.clear()
        self.humidity['text'] = kwargs['humidity']
        self.wind_direction['text'] = kwargs['windDir']
        self.wind_speed['text'] = kwargs['windSpeed']
        self.pressure['text'] = kwargs['pressure']
        self.visibility['text'] = kwargs['vis']
        self.cloud['text'] = kwargs['cloud']

    def clear(self):
        self.humidity['text'] = self.OCC
        self.wind_direction['text'] = self.OCC
        self.wind_speed['text'] = self.OCC
        self.pressure['text'] = self.OCC
        self.visibility['text'] = self.OCC
        self.cloud['text'] = self.OCC

class WindPage(SerialPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.wind_direction = tk.Label(self, text=self.OCC)
        self.wind_direction.grid(row=0, column=0, padx=10, pady=10)
        self.wind_speed = tk.Label(self, text=self.OCC)
        self.wind_speed.grid(row=0, column=1, padx=10, pady=10)
        self.wind_360 = tk.Label(self, text=self.OCC)
        self.wind_360.grid(row=0, column=2, padx=10, pady=10)
    
    def update(self, **kwargs):
        self.clear()
        self.wind_direction['text'] = kwargs['windDir']
        self.wind_speed['text'] = kwargs['windSpeed']
        self.wind_360['text'] = kwargs['wind360']

    def clear(self):
        self.wind_direction['text'] = self.OCC
        self.wind_speed['text'] = self.OCC
        self.wind_360['text'] = self.OCC

class IndexPage(SerialPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.scroll_canvas = tk.Canvas(self, scrollregion=(0, 0, 100, 300), width=200, height=150)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbar = tk.Scrollbar(self, command=self.scroll_canvas.xview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)
        
    def update(self, **kwargs):
        self.clear()
        today = kwargs['daily'][0]['date']
        for i in range(len(kwargs['daily'])):
            if kwargs['daily'][i]['date'] == today:
                label = tk.Label(self.scroll_canvas, text=f"{kwargs['daily'][i]['name']}: {kwargs['daily'][i]['category']}")
                self.scroll_canvas.create_window(50, i * 15, anchor=tk.W, window=label)
    
    def clear(self):
        self.scroll_canvas.delete("all")


class Chart7DaysPage(SerialPage):
    def __init__(self, parent):
        super().__init__(parent)

        self.fig = Figure(figsize=(1, 0.8), dpi=100)
        self.ax = self.fig.add_subplot(111)

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
        y1_span = max(y1) - min(y1)
        y2_span = max(y2) - min(y2)
        for i in range(len(data)):
            y_offset_1 = 10 if y1_span and (y1[i] - min(y1)) / y1_span < 0.9 else -20
            y_offset_2 = 10 if y2_span and (y2[i] - min(y2)) / y2_span < 0.9 else -20
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

class Chart24HoursPage(SerialPage):
    def __init__(self, parent):
        super().__init__(parent)

        self.fig = Figure(figsize=(35, 2), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Create a canvas and a scrollbar,
        # then embed Frame-FigureCanvasTkAgg in the canvas
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Create a Frame
        self.frame = tk.Frame(self.canvas, bg='white')
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        # Adjust figure size to fit the frame
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def update_size(self, *args):
        # Disable configure event to avoid infinite loop
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        # Make the frame fill the whole canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        # Minus 20 to avoid scroll bar
        canvas_height = max(1, canvas_height - 10)
        # print(canvas_width, canvas_height)
        self.frame.config(width=canvas_width * 6, height=canvas_height)

    def update(self, **kwargs):
        self.clear()
        self.update_size()
        self.fig.tight_layout(pad=0.1)
        self.ax.set_yticks([])
        # data is a list of dict
        data = kwargs['hourly']
        x = np.arange(len(data))
        y1 = [int(data[i]['temp']) for i in range(len(data))]

        self.ax.plot(x, y1, color='red')
        self.ax.scatter(x, y1, color='red')
        span = max(y1) - min(y1)
        for i in range(len(data)):
            y_offset = 10 if span and (y1[i] - min(y1)) / span < 0.9 else -20
            self.ax.annotate(str(y1[i]) + "°C", (x[i], y1[i]), textcoords="offset points", xytext=(0, y_offset),
                             ha='center', color='red')

        # 设置横轴刻度标签
        x_labels = [data[i]['fxTime'][11:16] for i in range(len(data))]
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(x_labels)  # Rotate x-axis labels for better visibility

        self.fig_canvas.draw()

    def clear(self):
        self.ax.clear()

class ChartRainPage(SerialPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.fig = Figure(figsize=(1, 0.8), dpi=100)
        self.ax = self.fig.add_subplot(111)
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
        self.fig.suptitle(title, fontsize=12, ha='left')

        self.canvas.draw()
    
    def clear(self):
        self.ax.clear()

class SerialDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_page = 0

        # 创建左右换页按钮
        self.prev_button = tk.Button(self, text="<", command=self.show_previous_page)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        # 创建页码标签
        # self.page_label = tk.Label(self, text="Page 1")
        # self.page_label.pack(side=tk.RIGHT, padx=10)

        # 创建窗口
        self.serial_pages = []

        self.next_button = tk.Button(self, text=">", command=self.show_next_page)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        # 窗口前页
        self.show_current_page()
        
    def add_page(self, page):
        self.serial_pages.append(page)
        # self.page_label['text'] = "Page {}".format(self.current_page + 1)
        self.show_current_page()

    def show_current_page(self):
        # 隐藏所有页
        for page in self.serial_pages:
            page.pack_forget()

        # 显示当前页
        if len(self.serial_pages) > 0:
            self.serial_pages[self.current_page].pack(fill=tk.BOTH, expand=True)

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()
        if self.current_page == 0:
            self.prev_button['state'] = tk.DISABLED
        self.next_button['state'] = tk.NORMAL

    def show_next_page(self):
        if self.current_page < len(self.serial_pages) - 1:
            self.current_page += 1
            self.show_current_page()
        if self.current_page == len(self.serial_pages) - 1:
            self.next_button['state'] = tk.DISABLED
        self.prev_button['state'] = tk.NORMAL


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
