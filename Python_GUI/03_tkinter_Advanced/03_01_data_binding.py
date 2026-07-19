# -*- coding: utf-8 -*-
"""
교재 예제 파일: 데이터 상태와 바인딩
"""

import tkinter as tk

def show_result():
    label.config(text="난이도 : " + level_var.get())

root = tk.Tk()
level_var = tk.StringVar(value="쉬움")

for level in ["쉬움", "보통", "어려움"]:
    tk.Radiobutton(root, text=level, variable=level_var, value=level,
                   command=show_result).pack(anchor="w")

label = tk.Label(root, text="")
label.pack(pady=10)

root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# 
# message = tk.StringVar()
# message.set("데이터 상태와 바인딩")
# 
# label = tk.Label(root, textvariable=message)
# label.pack(padx=20, pady=20)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# 
# floor = tk.IntVar()
# floor.set(1)
# 
# label = tk.Label(root, textvariable=floor, font=("맑은 고딕", 30))
# label.pack(padx=30, pady=20)
# 
# def go_up():
#     floor.set(floor.get() + 1)
# 
# button_up = tk.Button(root, text="올라가기", command=go_up, width=10)
# button_up.pack(pady=5)
# 
# root.mainloop()

# [코드 조각]
# my_var = tk.StringVar()        # 먼저 변수 클래스로 만든다
# 
# my_var.set("변수 클래스")        # 값 넣기
# current_value = my_var.get()   # 값 읽기
