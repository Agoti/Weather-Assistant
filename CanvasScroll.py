import tkinter as tk

def on_scroll(*args):
    canvas.xview(*args)

root = tk.Tk()
root.title("Scrollable Canvas Example")

# 创建Canvas
canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack(expand=True, fill="both")

# 创建一个Frame，宽度为canvas的两倍
frame_width = 600
frame = tk.Frame(canvas, width=frame_width, height=200, bg="lightblue")
canvas.create_window((0, 0), window=frame, anchor="nw")

# 创建水平滑动条
scrollbar = tk.Scrollbar(root, orient="horizontal", command=on_scroll)
scrollbar.pack(fill="x")

# 设置Canvas与滑动条的关联
canvas.configure(xscrollcommand=scrollbar.set)

# 配置Canvas的可滚动范围
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()
