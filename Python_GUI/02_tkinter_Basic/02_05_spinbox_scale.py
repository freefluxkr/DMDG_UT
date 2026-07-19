# -*- coding: utf-8 -*-
"""
교재 예제 파일: 스핀박스, 스케일
"""

import tkinter as tk

def show_month():
    label.config(text="선택한 달: " + spinbox.get())

root = tk.Tk()
root.title("문자열 Spinbox")

spinbox = tk.Spinbox(root, values=("1월", "2월", "3월", "4월", "5월"), width=10)
spinbox.pack(padx=10, pady=10)

button = tk.Button(root, text="확인", command=show_month)
button.pack(pady=5)

label = tk.Label(root, text="")
label.pack(pady=10)

root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# def show_value():
#     label.config(text="선택한 수량: " + spinbox.get())
# 
# root = tk.Tk()
# root.title("Spinbox 예제")
# 
# spinbox = tk.Spinbox(root, from_=1, to=10, width=10)
# spinbox.pack(padx=10, pady=10)
# 
# button = tk.Button(root, text="확인", command=show_value)
# button.pack(pady=5)
# 
# label = tk.Label(root, text="")
# label.pack(pady=10)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# def show_value():
#     label.config(text="선택한 볼륨: " + str(scale.get()))
# 
# root = tk.Tk()
# 
# scale = tk.Scale(root, from_=0, to=100, orient="horizontal")
# scale.pack(padx=10, pady=10)
# 
# button = tk.Button(root, text="확인", command=show_value)
# button.pack(pady=5)
# 
# label = tk.Label(root, text="")
# label.pack(pady=10)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# def show_value():
#     label.config(text=f"선택한 밝기: {scale.get()}")
# 
# root = tk.Tk()
# 
# scale = tk.Scale(root, from_=0, to=100, orient="vertical")
# scale.pack(pady=10)
# 
# tk.Button(root, text="확인", command=show_value).pack()
# 
# label = tk.Label(root)
# label.pack(pady=10)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# def change_value(value):
#     label.config(text=f"현재 값: {value}")
# 
# root = tk.Tk()
# 
# scale = tk.Scale(root, from_=0, to=100, orient="horizontal", command=change_value)
# scale.pack(pady=10)
# 
# label = tk.Label(root, text="현재 값: 0")
# label.pack(pady=10)
# 
# root.mainloop()
