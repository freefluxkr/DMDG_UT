# -*- coding: utf-8 -*-
"""
교재 예제 파일: GUI 창 띄우기
"""

import tkinter as tk

root = tk.Tk()
root.geometry("400x300")
root.minsize(300, 200)
root.maxsize(800, 600)

root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk  
# 
# root = tk.Tk()
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.title("이곳이 제목 표시줄")
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("200x50")
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.title("창 위치 설정")
# root.geometry("400x300+100+200")
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("200x50")
# root.configure(bg="lightblue")
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("400x300")
# root.resizable(False, False)
# 
# root.mainloop()
