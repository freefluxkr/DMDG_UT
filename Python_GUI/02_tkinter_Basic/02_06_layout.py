# -*- coding: utf-8 -*-
"""
교재 예제 파일: 레이아웃 관리자
"""

import tkinter as tk

root = tk.Tk()
root.geometry("360x150")
root.configure(bg="#797777")

# 위쪽 프레임: 입력 폼 (내부는 grid)
top = tk.Frame(root, bg="#d7ecff", padx=5, pady=5)
top.pack(side="top", fill="x", padx=5, pady=5)

tk.Label(top, text="이메일 주소", bg="#d7ecff").grid(row=0, column=0, sticky="w", padx=(0, 8))
tk.Entry(top, bg="white").grid(row=0, column=1, sticky="we")
top.grid_columnconfigure(1, weight=1)  # 입력칸이 가로로 늘어나도록

# 아래쪽 프레임: 버튼 (내부는 pack)
bottom = tk.Frame(root, bg="#ffe0e0", padx=5, pady=5)
bottom.pack(side="bottom", fill="x", padx=5, pady=5)

tk.Button(bottom, text="확인", bg="#7bc96f", fg="white", width=8).pack(side="left")
tk.Button(bottom, text="취소", bg="#e87a7a", fg="white", width=8).pack(side="right")

root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("200x150")
# 
# tk.Label(root, text="첫 번째 라벨 위젯", bg="red").pack()
# tk.Label(root, text="두 번째 라벨 위젯", bg="green").pack()
# tk.Label(root, text="세 번째 라벨 위젯", bg="yellow").pack()
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("400x300")
# 
# tk.Button(root, text="LEFT").pack(side="left")
# tk.Button(root, text="RIGHT").pack(side="right")
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("250x120")
# 
# tk.Button(root, text="가로만 채우기").pack(fill="x")
# tk.Button(root, text="전체 확장").pack(expand=True, fill="both")
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("180x50")
# 
# tk.Label(root, text="이름").grid(row=0, column=0)
# tk.Entry(root).grid(row=0, column=1)
# tk.Label(root, text="나이").grid(row=1, column=0)
# tk.Entry(root).grid(row=1, column=1)
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.grid_columnconfigure(1, weight=1)      # 1번 열만 늘어남
# 
# opt = {"padx": 5, "pady": 5}
# tk.Label(root, text="이메일 주소", bg="lightblue").grid(row=1, column=0, sticky="w", **opt)            # 왼쪽 정렬
# tk.Entry(root, bg="lightyellow").grid(row=1, column=1, sticky="we", **opt)                      # 좌우로 꽉 참
# tk.Button(root, text="로그인", bg="lightgreen").grid(row=2, columnspan=2, sticky="we", **opt)  # 두 열 차지
# 
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.geometry("300x150")
# 
# tk.Label(root, text="절대 위치 (50, 30)", bg="lightblue").place(x=50, y=30) # 절대 좌표 배치 (x, y는 픽셀)
# 
# tk.Label(root, text="상대 좌표 배치 (정중앙)", bg="lightgreen").place(
#     relx=0.5, rely=0.5, anchor="center"
# ) # 상대 좌표 배치 (relx, rely는 0.0 ~ 1.0 비율)
# 
# tk.Label(root, text="상대 크기 지정 (너비 80%)", bg="lightyellow").place(
#     relx=0.1, rely=0.8, relwidth=0.8
# ) # 상대 크기 지정 (relwidth, relheight)
# 
# root.mainloop()
