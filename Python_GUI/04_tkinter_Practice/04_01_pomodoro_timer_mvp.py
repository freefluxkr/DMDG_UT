# -*- coding: utf-8 -*-
"""
교재 예제 파일: 뽀모도로 타이머 최소 기능
"""

import tkinter as tk

class PomodoroTimer:
    BG = "#e63946"

    def __init__(self, root):
        self.root = root
        self.running = False
        self.minutes = tk.IntVar(value=25)          # 선택된 분(20/25/30)
        self.remaining = self.minutes.get() * 60
        root.config(bg=self.BG)

        self.label = tk.Label(root, text="25:00", font=("Arial", 60),
                              fg="white", bg=self.BG)
        self.label.pack(padx=40, pady=(0, 10))

        radios = tk.Frame(root, bg=self.BG)
        radios.pack()
        for m in (20, 25, 30):
            tk.Radiobutton(radios, text=f"{m}분", value=m, variable=self.minutes,
                           command=self.set_time, bg=self.BG, fg="white",
                           selectcolor=self.BG, activebackground=self.BG,
                           activeforeground="white").pack(side="left", padx=5)

        frame = tk.Frame(root, bg=self.BG)
        frame.pack(pady=20)
        tk.Button(frame, text="시작", command=self.start).pack(side="left", padx=5)
        tk.Button(frame, text="리셋", command=self.reset).pack(side="left", padx=5)

    def update_label(self):
        m, s = divmod(self.remaining, 60)
        self.label.config(text=f"{m:02d}:{s:02d}")

    def set_time(self):                              # 라디오 선택 시 호출
        self.running = False
        self.remaining = self.minutes.get() * 60
        self.update_label()

    def tick(self):
        if self.running and self.remaining > 0:
            self.remaining -= 1
            self.update_label()
            self.root.after(1000, self.tick)

    def start(self):
        if not self.running:
            self.running = True
            self.tick()

    def reset(self):
        self.set_time()

root = tk.Tk()
root.title("뽀모도로 v0.3")
PomodoroTimer(root)
root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# remaining = 25 * 60
# 
# def tick():
#     global remaining
#     m, s = divmod(remaining, 60)
#     label.config(text=f"{m:02d}:{s:02d}")
#     if remaining > 0:
#         remaining -= 1
#         root.after(1000, tick)
# 
# root = tk.Tk()
# root.title("뽀모도로 v0.1")
# label = tk.Label(root, text="25:00", font=("Arial", 48))
# label.pack(padx=40, pady=20)
# tk.Button(root, text="시작", command=tick).pack(pady=10)
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# class PomodoroTimer:
#     WORK_MIN = 25
# 
#     def __init__(self, root):
#         self.root = root
#         self.remaining = self.WORK_MIN * 60
#         self.running = False
# 
#         self.label = tk.Label(root, text="25:00", font=("Arial", 48))
#         self.label.pack(padx=40, pady=20)
# 
#         frame = tk.Frame(root)
#         frame.pack(pady=10)
#         tk.Button(frame, text="시작", command=self.start).pack(side="left", padx=5)
#         tk.Button(frame, text="리셋", command=self.reset).pack(side="left", padx=5)
# 
#     def update_label(self):
#         m, s = divmod(self.remaining, 60)
#         self.label.config(text=f"{m:02d}:{s:02d}")
# 
#     def tick(self):
#         if self.running and self.remaining > 0:
#             self.remaining -= 1
#             self.update_label()
#             self.root.after(1000, self.tick)
# 
#     def start(self):
#         if not self.running:
#             self.running = True
#             self.tick()
# 
#     def reset(self):
#         self.running = False
#         self.remaining = self.WORK_MIN * 60
#         self.update_label()
# 
# root = tk.Tk()
# root.title("뽀모도로 v0.2")
# PomodoroTimer(root)
# root.mainloop()

# [코드 조각]
# def tick():
#     global remaining

# [코드 조각]
# def __init__(self, root):
#     self.root = root
#     self.remaining = self.WORK_MIN * 60
#     self.running = False

# [코드 조각]
# def start(self):
#     if not self.running:        # 이미 돌면 무시
#         self.running = True
#         self.tick()

# [코드 조각]
# def reset(self):
#     self.running = False
#     self.remaining = self.WORK_MIN * 60
#     self.update_label()

# [코드 조각]
# self.minutes = tk.IntVar(value=25)
# self.remaining = self.minutes.get() * 60

# [코드 조각]
# self.label = tk.Label(root, text="25:00", font=("Arial", 60),
#                       fg="white", bg=self.BG)
# self.label.pack(padx=40, pady=(0, 10))

# [코드 조각]
# for m in (20, 25, 30):
#     tk.Radiobutton(radios, text=f"{m}분", value=m, variable=self.minutes,
#                    command=self.set_time, bg=self.BG, fg="white",
#                    selectcolor=self.BG, activebackground=self.BG,
#                    activeforeground="white").pack(side="left", padx=5)

# [코드 조각]
# def set_time(self):
#     self.running = False
#     self.remaining = self.minutes.get() * 60
#     self.update_label()
