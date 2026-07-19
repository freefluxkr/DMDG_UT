# -*- coding: utf-8 -*-
"""
교재 예제 파일: ttk 위젯과 스타일링
"""

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()

frm = ttk.Frame(root, padding=20)
frm.pack()

cur = tk.StringVar(value=style.theme_use())
cb = ttk.Combobox(frm, values=style.theme_names(), textvariable=cur, state="readonly")
cb.pack(pady=5)
cb.bind("<<ComboboxSelected>>", lambda e: style.theme_use(cur.get()))

ttk.Button(frm, text="버튼").pack(pady=5)
ttk.Checkbutton(frm, text="체크박스").pack(pady=5)
ttk.Progressbar(frm, value=60).pack(pady=5)

root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# from tkinter import ttk
# 
# root = tk.Tk()
# 
# label = ttk.Label(root, text="이름 : ")
# label.grid(row=0, column=0, padx=5, pady=5)
# 
# entry = ttk.Entry(root)
# entry.grid(row=0, column=1, padx=5, pady=5)
# 
# button = ttk.Button(root, text="확인", command=lambda: print(entry.get()))
# button.grid(row=1, column=0, columnspan=2, pady=5)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# from tkinter import ttk
# 
# root = tk.Tk()
# 
# style = ttk.Style()
# style.configure("TButton", font=("맑은 고딕", 11), padding=6)
# style.configure("Accent.TButton", foreground="lightgreen", background="green")
# 
# btn1 = ttk.Button(root, text="기본 버튼")
# btn1.pack(padx=50, pady=5)
# 
# btn2 = ttk.Button(root, text="강조 버튼", style="Accent.TButton")
# btn2.pack(padx=50, pady=5)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# from tkinter import ttk
# 
# root = tk.Tk()
# 
# style = ttk.Style()
# print(style.theme_names())
# print(style.theme_use())
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# from tkinter import ttk
# 
# root = tk.Tk()
# 
# style = ttk.Style()
# style.theme_use("clam")
# 
# style.map("TButton",
#     background=[("active", "lightblue"),
#                 ("pressed", "blue"),
#                 ("disabled", "lightyellow")],
#     foreground=[("disabled", "gray")])
# 
# ttk.Button(root, text="마우스를 올려보세요").pack(padx=20, pady=10)
# ttk.Button(root, text="비활성 버튼", state="disabled").pack(padx=20, pady=10)
# 
# root.mainloop()

# [코드 조각]
# btn1 = ttk.Button(root, text="기본 버튼")

# [코드 조각]
# btn2 = ttk.Button(root, text="강조 버튼", style="Accent.TButton")

# [코드 조각]
# cur = tk.StringVar(value=style.theme_use())

# [코드 조각]
# cb = ttk.Combobox(frm, values=style.theme_names(), textvariable=cur, state="readonly")
