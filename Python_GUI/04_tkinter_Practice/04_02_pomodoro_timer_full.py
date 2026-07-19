# -*- coding: utf-8 -*-
"""
교재 예제 파일: 뽀모도로 타이머 완성
"""

import tkinter as tk

class PomodoroTimer:
    COLOR = "#e63946"
    SIZE = 250   # 캔버스 한 변 길이(px)

    def __init__(self, root):
        self.root = root
        self.running = False
        self.minutes = tk.IntVar(value=25)          # 선택된 분(20/25/30)
        self.total = self.minutes.get() * 60
        self.remaining = self.total

        self.canvas = tk.Canvas(root, width=self.SIZE, height=self.SIZE,
                                highlightthickness=0)
        self.canvas.pack(pady=15)

        radios = tk.Frame(root)
        radios.pack()
        for m in (20, 25, 30):
            tk.Radiobutton(radios, text=f"{m}분", value=m, variable=self.minutes,
                           command=self.set_time).pack(side="left", padx=5)

        frame = tk.Frame(root)
        frame.pack(pady=(5, 15))
        tk.Button(frame, text="시작", command=self.start).pack(side="left", padx=5)
        tk.Button(frame, text="리셋", command=self.reset).pack(side="left", padx=5)

        self.draw()

    def set_time(self):                              # 라디오 선택 시 호출
        self.running = False
        self.total = self.minutes.get() * 60
        self.remaining = self.total
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        pad = 10
        box = (pad, pad, self.SIZE - pad, self.SIZE - pad)
        self.canvas.create_oval(*box, fill="white", outline="#dddddd")

        frac = self.remaining / self.total           # 남은 비율 (1 → 0)
        if frac >= 1:
            self.canvas.create_oval(*box, fill=self.COLOR, outline="")
        elif frac > 0:                                # 12시 방향에서 시계방향으로
            self.canvas.create_arc(*box, start=90, extent=-360 * frac,
                                   fill=self.COLOR, outline="")

        m, s = divmod(self.remaining, 60)
        self.canvas.create_text(self.SIZE // 2, self.SIZE // 2,
                                text=f"{m:02d}:{s:02d}", font=("Arial", 36))

    def tick(self):
        if self.running and self.remaining > 0:
            self.remaining -= 1
            self.draw()
            self.root.after(1000, self.tick)

    def start(self):
        if not self.running:
            self.running = True
            self.tick()

    def reset(self):
        self.set_time()

root = tk.Tk()
root.title("뽀모도로 v0.4")
PomodoroTimer(root)
root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# COLOR = "#e63946"
# total = 1 * 60
# remaining = total
# 
# def draw():
#     global remaining
#     canvas.delete("all")
#     box = (10, 10, 240, 240)
#     canvas.create_oval(*box, fill="white", outline="#dddddd")
# 
#     frac = remaining / total
#     if frac >= 1:
#         canvas.create_oval(*box, fill=COLOR, outline="")
#     elif frac > 0:
#         canvas.create_arc(*box, start=90, extent=-360 * frac,
#                           fill=COLOR, outline="")
# 
#     if remaining > 0:
#         remaining-= 1
#         root.after(1000, draw)
# 
# 
# root = tk.Tk()
# canvas = tk.Canvas(root, width=250, height=250, highlightthickness=0)
# canvas.pack(padx=20, pady=20)
# draw()
# root.mainloop()

# [코드 조각]
# self.canvas = tk.Canvas(root, width=self.SIZE, height=self.SIZE,
#                         highlightthickness=0)
# self.canvas.pack(pady=15)

# [코드 조각]
# self.total = self.minutes.get() * 60
# self.remaining = self.total

# [코드 조각]
# m, s = divmod(self.remaining, 60)
# self.canvas.create_text(self.SIZE // 2, self.SIZE // 2,
#                         text=f"{m:02d}:{s:02d}", font=("Arial", 36))
