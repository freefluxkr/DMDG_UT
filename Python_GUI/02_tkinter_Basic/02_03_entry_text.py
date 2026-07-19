# -*- coding: utf-8 -*-
"""
교재 예제 파일: 엔트리와 텍스트
"""

import tkinter as tk

def change_text():
    text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, text.upper())

root = tk.Tk()

entry = tk.Entry(root)
entry.pack(padx=10, pady=10)

button = tk.Button(root, text="대문자로 변경", command=change_text)
button.pack(padx=10, pady=10)

root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# 
# password_entry = tk.Entry(root, show="*", width=30)
# password_entry.pack(pady=20)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# 
# text = tk.Text(root)
# text.pack(pady=10)
# 
# root.mainloop()
