import tkinter as tk

def on_scroll(*args):
    canvas.yview(*args)

root = tk.Tk()
root.title("Scrollbar with Labels")

# 创建带有垂直滚动条的Canvas
canvas = tk.Canvas(root, scrollregion=(0, 0, 100, 300), width=200, height=150)
canvas.pack(side=tk.LEFT, fill=tk.Y)

# 创建垂直滚动条并绑定到Canvas
scrollbar = tk.Scrollbar(root, command=on_scroll)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.config(yscrollcommand=scrollbar.set)

# 添加一些标签到Canvas
for i in range(20):
    label = tk.Label(canvas, text=f"Label {i}")
    canvas.create_window(50, i * 15, anchor=tk.W, window=label)

root.mainloop()
