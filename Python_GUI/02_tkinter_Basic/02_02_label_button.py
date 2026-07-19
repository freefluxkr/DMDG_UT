# -*- coding: utf-8 -*-
"""
교재 예제 파일: 라벨과 버튼
"""

import tkinter as tk

root = tk.Tk()

btn1 = tk.Button(root, text="두꺼운 테두리", bd=5, relief="raised", width=15)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="커서 변경 (손가락)", cursor="hand2", bg="lightyellow")
btn2.pack(pady=5)

btn3 = tk.Button(root, text="클릭 불가", state="disabled")
btn3.pack(pady=5)

root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# 
# label = tk.Label(root, text="라벨입니다.")
# label.pack()
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# 
# label = tk.Label(
#     root,
#     text="Python GUI",
#     font=("맑은 고딕", 16),
#     fg="white",
#     bg="navy"
# )
# label.pack(padx=40,pady=10)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# def hello():
#     label.config(text="버튼을 클릭했습니다!")
# 
# root = tk.Tk()
# 
# label = tk.Label(root, text="버튼을 눌러보세요", padx=40, pady=10)
# label.pack()
# 
# button = tk.Button(root, text="클릭", command=hello)
# button.pack()
# 
# root.mainloop()

# [코드 조각]
# label = tk.Label(root, text="라벨입니다.")
# label.pack()

# [코드 조각]
# def hello():
#     label.config(text="버튼을 클릭했습니다!")
# 
# button = tk.Button(root, text="클릭", command=hello)

# [코드 조각]
# button = tk.Button(root, text="클릭", command=hello)
# 
# def hello():
#     print("Hello")
