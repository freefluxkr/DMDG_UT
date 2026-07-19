# -*- coding: utf-8 -*-
"""
교재 예제 파일: JSON 연락처 관리
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os, json

FILE = "contacts.json"

def load():
    if os.path.exists(FILE):
        with open(FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

def save():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

def refresh():
    tree.delete(*tree.get_children())
    for c in contacts:
        tree.insert("", "end", values=(c["name"], c["company"], c["phone"]))

def add():
    name, company, phone = e_name.get(), e_company.get(), e_phone.get()
    if not name:
        messagebox.showwarning("확인", "이름을 입력하세요.")
        return
    contacts.append({"name": name, "company": company, "phone": phone})
    save()
    refresh()
    for e in (e_name, e_company, e_phone):
        e.delete(0, "end")

def delete():
    sel = tree.selection()
    if not sel:
        return
    idx = tree.index(sel[0])
    contacts.pop(idx)
    save()
    refresh()

contacts = load()

root = tk.Tk()
root.title("연락처 v0.2")

input_frame = tk.LabelFrame(root, text="입력", padx=10, pady=10)
input_frame.pack(padx=10, pady=10, fill="x")

tk.Label(input_frame, text="이름").grid(row=0, column=0)
tk.Label(input_frame, text="회사").grid(row=0, column=1)
tk.Label(input_frame, text="전화").grid(row=0, column=2)

e_name = tk.Entry(input_frame)
e_company = tk.Entry(input_frame)
e_phone = tk.Entry(input_frame)
e_name.grid(row=1, column=0, padx=2)
e_company.grid(row=1, column=1, padx=2)
e_phone.grid(row=1, column=2, padx=2)

tk.Button(input_frame, text="추가", command=add).grid(row=1, column=3, padx=5)
tk.Button(input_frame, text="삭제", command=delete).grid(row=1, column=4)

list_frame = tk.LabelFrame(root, text="목록", padx=10, pady=10)
list_frame.pack(padx=10, pady=(0, 10), fill="both")

tree = ttk.Treeview(list_frame, columns=("name", "company", "phone"), show="headings", height=8)
tree.heading("name", text="이름")
tree.heading("company", text="회사")
tree.heading("phone", text="전화")
tree.pack()

refresh()
root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# import os, json
# 
# FILE = "contacts.json"
# 
# def load():
#     if os.path.exists(FILE):
#         with open(FILE, encoding="utf-8") as f:
#             return json.load(f)
#     return []
# 
# def save():
#     with open(FILE, "w", encoding="utf-8") as f:
#         json.dump(contacts, f, ensure_ascii=False, indent=2)
# 
# def add():
#     contacts.append({
#         "name": e_name.get(),
#         "company": e_company.get(),
#         "phone": e_phone.get(),
#     })
#     save()
# 
# contacts = load()
# 
# root = tk.Tk()
# root.title("연락처 v0.1")
# 
# tk.Label(root, text="이름").grid(row=0, column=0)
# tk.Label(root, text="회사").grid(row=0, column=1)
# tk.Label(root, text="전화").grid(row=0, column=2)
# 
# e_name = tk.Entry(root)
# e_company = tk.Entry(root)
# e_phone = tk.Entry(root)
# e_name.grid(row=1, column=0)
# e_company.grid(row=1, column=1)
# e_phone.grid(row=1, column=2)
# 
# tk.Button(root, text="추가", command=add).grid(row=3, column=1)
# 
# root.mainloop()

# [코드 조각]
# import os, json
# 
# FILE = "contacts.json"
# 
# def load():
#     if os.path.exists(FILE):
#         with open(FILE, encoding="utf-8") as f:
#             return json.load(f)
#     return []
# 
# def save():
#     with open(FILE, "w", encoding="utf-8") as f:
#         json.dump(contacts, f, ensure_ascii=False, indent=2)
# 
# contacts = load()
# save()

# [코드 조각]
# tree = ttk.Treeview(list_frame, columns=("name", "company", "phone"), show="headings", height=8)
