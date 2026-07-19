# -*- coding: utf-8 -*-
"""
교재 예제 파일: 절차적 코드의 한계
"""

import tkinter as tk

root = tk.Tk()
root.geometry("300x400")

total_count = 0
done_count = 0

listbox = tk.Listbox(root)
listbox.pack(fill="both", expand=True, padx=10, pady=(0, 7))

entry = tk.Entry(root)
entry.pack(fill="x", padx=10, pady=10)

status_label = tk.Label(root, text="전체 0개 / 완료 0개")
status_label.pack()

def update_status():
    global total_count, done_count
    status_label.config(text=f"전체 {total_count}개 / 완료 {done_count}개")

def add_item():
    global total_count
    text = entry.get().strip()
    if text:
        listbox.insert(tk.END, text)
        entry.delete(0, tk.END)
        total_count += 1
        update_status()

def delete_item():
    global total_count
    selected = listbox.curselection()
    if selected:
        listbox.delete(selected[0])
        total_count -= 1
        update_status()

def mark_done():
    global done_count
    selected = listbox.curselection()
    if selected:
        text = listbox.get(selected[0])
        listbox.delete(selected[0])
        listbox.insert(selected[0], "[완료] " + text)
        done_count += 1
        update_status()

def clear_all():
    global total_count, done_count
    listbox.delete(0, tk.END)
    total_count = 0
    done_count = 0
    update_status()

add_button = tk.Button(root, text="추가", command=add_item)
add_button.pack()

done_button = tk.Button(root, text="완료 처리", command=mark_done)
done_button.pack()

delete_button = tk.Button(root, text="삭제", command=delete_item)
delete_button.pack()

clear_button = tk.Button(root, text="전체 비우기", command=clear_all)
clear_button.pack()

root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("300x250")
# 
# listbox = tk.Listbox(root)
# listbox.pack(fill="both", expand=True, padx=10, pady=(0, 7))
# 
# entry = tk.Entry(root)
# entry.pack(fill="x", padx=10, pady=10)
# 
# def add_item():
#     text = entry.get().strip()
#     if text:
#         listbox.insert(tk.END, text)
#         entry.delete(0, tk.END)
# 
# button = tk.Button(root, text="추가", command=add_item)
# button.pack(pady=(0, 10))
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("300x250")
# 
# listbox = tk.Listbox(root)
# listbox.pack(fill="both", expand=True, padx=10, pady=(0, 7))
# 
# entry = tk.Entry(root)
# entry.pack(fill="x", padx=10, pady=10)
# 
# def add_item():
#     text = entry.get().strip()
#     if text:
#         listbox.insert(tk.END, text)
#         entry.delete(0, tk.END)
# 
# def delete_item():
#     selected_indices = listbox.curselection()
#     if selected_indices:
#         listbox.delete(selected_indices[0])
# 
# add_button = tk.Button(root, text="추가", command=add_item)
# add_button.pack(pady=(0, 5))
# 
# delete_button = tk.Button(root, text="삭제", command=delete_item)
# delete_button.pack(pady=(0, 10))
# 
# root.mainloop()

# [코드 조각]
# def add_item():
#     text = entry.get().strip()
#     if text:
#         listbox.insert(tk.END, text)
#         entry.delete(0, tk.END)

# [코드 조각]
# def delete_item():
#     selected_indices = listbox.curselection()
#     if selected_indices:
#         listbox.delete(selected_indices[0])

# [코드 조각]
# def update_status():
#     global total_count, done_count
#     status_label.config(text=f"전체 {total_count}개 / 완료 {done_count}개")

# [코드 조각]
# def mark_done():
#     # global done_count  ← 이 줄을 빠뜨리면?
#     done_count += 1      # 에러는 없지만, 카운터가 증가하지 않습니다.
