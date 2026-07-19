# -*- coding: utf-8 -*-
"""
교재 예제 파일: ttk 고유 위젯
"""

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
tree = ttk.Treeview(root, columns=("item", "spec", "price"), show="headings")
tree.heading("item", text="제품")
tree.heading("spec", text="스펙")
tree.heading("price", text="가격")

data = [("가방", "16인치", 123), ("청소기", "700W", 250), ("운동화", "275mm", 54)]
for item, spec, price in data:
    tree.insert("", "end", values=(item, spec, price))

tree.pack(padx=5, pady=5, expand=True, fill="both")
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
# combo = ttk.Combobox(root, values=["서울", "부산", "대구"])
# combo.set("서울")
# combo.bind("<<ComboboxSelected>>", lambda e: print(combo.get()))
# combo.pack(padx=20, pady=20)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# from tkinter import ttk
# 
# root = tk.Tk()
# 
# pb = ttk.Progressbar(root, length=200, mode="determinate", maximum=100)
# pb.pack(padx=20, pady=20)
# pb["value"] = 0
# 
# def step():
#     pb["value"] = (pb["value"] + 10) % 110
# 
# ttk.Button(root, text="+10", command=step).pack(pady=5)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# from tkinter import ttk
# 
# root = tk.Tk()
# root.geometry("300x150")
# 
# notebook = ttk.Notebook(root)
# frame1 = ttk.Frame(notebook, width=300, height=150)
# frame2 = ttk.Frame(notebook, width=300, height=150)
# 
# ttk.Label(frame1, text="메인 페이지 내용").pack(padx=10, pady=10)
# ttk.Label(frame2, text="설정 페이지 내용").pack(padx=10, pady=10)
# 
# notebook.add(frame1, text="메인")
# notebook.add(frame2, text="설정")
# notebook.pack(expand=True, fill="both")
# 
# root.mainloop()
