# -*- coding: utf-8 -*-
"""
교재 예제 파일: 메뉴 바 구성
"""

import tkinter as tk

root = tk.Tk()
root.geometry("400x120")

menubar = tk.Menu(root)    # 1) 메뉴바 생성

file_menu = tk.Menu(menubar, tearoff=0)    # 2) 하위 메뉴 생성
file_menu.add_command(label="열기", command=lambda: print("열기 클릭"))    # 3) 항목 채우기
file_menu.add_separator()
file_menu.add_command(label="종료", command=root.destroy)

menubar.add_cascade(label="파일", menu=file_menu)    # 4) 메뉴바에 연결

root.config(menu=menubar)    # 5) 창에 부착
root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("300x120")
# 
# menu = tk.Menu(root, tearoff=0)
# menu.add_command(label="복사", command=lambda: print("복사"))
# menu.add_command(label="붙여넣기", command=lambda: print("붙여넣기"))
# 
# label = tk.Label(root, text="이 글자 위에서 오른쪽 클릭", bg="lightyellow")
# label.pack(pady=30)
# 
# label.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))
# 
# root.mainloop()
