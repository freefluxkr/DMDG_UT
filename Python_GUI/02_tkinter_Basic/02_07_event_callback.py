# -*- coding: utf-8 -*-
"""
교재 예제 파일: 이벤트와 콜백
"""

import tkinter as tk

def on_key(event):
    result_label.config(text=f"입력된 키 : {event.char}")

root = tk.Tk()

entry = tk.Entry(root, width=30)
entry.pack(padx=20, pady=10)

result_label = tk.Label(root, text="입력된 키 : ", bg="lightyellow")
result_label.pack(padx=20, pady=10)

entry.bind("<Key>", on_key)

root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [코드 조각]
# def on_key(event):
#     result_label.config(text=f"입력된 키 : {event.char}")
