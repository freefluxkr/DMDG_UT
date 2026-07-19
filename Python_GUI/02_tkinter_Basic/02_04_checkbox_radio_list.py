# -*- coding: utf-8 -*-
"""
교재 예제 파일: 체크, 라디오, 리스트
"""

import tkinter as tk

def show_selected(event):
    label.config(text="선택한 항목: " + listbox.get(listbox.curselection()))

root = tk.Tk()
listbox = tk.Listbox(root, height=5)
listbox.pack(padx=10, pady=10)

for item in ["Python", "Java", "JavaScript", "C", "C++"]:
    listbox.insert(tk.END, item)

listbox.bind("<<ListboxSelect>>", show_selected)

label = tk.Label(root, text="")
label.pack(pady=10)

root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# def show_result():
#     if agree_var.get():
#         label.config(text="동의했습니다.")
# 
# root = tk.Tk()
# agree_var = tk.BooleanVar()
# 
# check = tk.Checkbutton(root, text="동의합니다", variable=agree_var, command=show_result)
# check.pack(padx=20, pady=20)
# 
# label = tk.Label(root, text="")
# label.pack(pady=10)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# 
# food = tk.IntVar(value=1)
# 
# tk.Radiobutton(root, text="육고기", variable=food, value=1).pack()
# tk.Radiobutton(root, text="해산물", variable=food, value=2).pack()
# 
# root.mainloop()
