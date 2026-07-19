# -*- coding: utf-8 -*-
"""
교재 예제 파일: 큐(Queue) 통신
"""

import tkinter as tk
import threading
import queue
import time


class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.queue = queue.Queue()
        self.label = tk.Label(root, text="10", font=("Arial", 60))
        self.label.pack(expand=True)
        tk.Button(root, text="시작", command=self.start).pack(pady=10)
        self.poll()

    def start(self):
        threading.Thread(target=self.count, daemon=True).start()

    def count(self):
        for i in range(10, -1, -1):
            self.queue.put(str(i))
            time.sleep(1)
        self.queue.put("끝!")

    def poll(self):
        try:
            while True:
                self.label.config(text=self.queue.get_nowait())
        except queue.Empty:
            pass
        self.root.after(100, self.poll)


if __name__ == "__main__":
    root = tk.Tk()
    CountdownApp(root)
    root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# import threading
# import queue
# import time
# 
# root = tk.Tk()
# label = tk.Label(root, text="대기 중", font=("", 20))
# label.pack(padx=40, pady=40)
# 
# q = queue.Queue()
# 
# 
# def work():
#     for i in range(1, 10):
#         time.sleep(1)
#         q.put(i)
# 
# 
# def poll():
#     try:
#         while True:
#             n = q.get_nowait()
#             label.config(text=f"{n} 초")
#     except queue.Empty:
#         pass
#     root.after(100, poll)
# 
# 
# threading.Thread(target=work, daemon=True).start()
# root.after(100, poll)
# root.mainloop()

# [코드 조각]
# import queue
# q = queue.Queue()          # 크기 제한 없는 큐
# q = queue.Queue(maxsize=5) # 최대 5개까지만 담는 큐

# [코드 조각]
# def work():
#     for i in range(1, 10):
#         time.sleep(1)
#         q.put(i)

# [코드 조각]
# def poll():
#     try:
#         while True:
#             n = q.get_nowait()
#             label.config(text=f"{n} 초")
#     except queue.Empty:
#         pass
#     root.after(100, poll)
