# -*- coding: utf-8 -*-
"""
교재 예제 파일: GUI와 멀티스레드
"""

import tkinter as tk
import threading
import time


class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.label = tk.Label(root, text="10", font=("Arial", 60))
        self.label.pack(expand=True)
        tk.Button(root, text="시작", command=self.start).pack(pady=10)

    def start(self):
        threading.Thread(target=self.count, daemon=True).start()

    def count(self):
        for i in range(10, -1, -1):
            self.label.config(text=str(i))
            time.sleep(1)
        self.label.config(text="끝!")


if __name__ == "__main__":
    root = tk.Tk()
    CountdownApp(root)
    root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# import time
# 
# 
# class CountdownApp:
#     def __init__(self, root):
#         self.root = root
#         self.label = tk.Label(root, text="10", font=("Arial", 60))
#         self.label.pack(expand=True)
#         tk.Button(root, text="시작", command=self.start).pack(pady=10)
# 
#     def start(self):
#         for i in range(10, -1, -1):
#             self.label.config(text=str(i))
#             self.root.update_idletasks()
#             time.sleep(1)
#         self.label.config(text="끝!")
# 
# 
# if __name__ == "__main__":
#     root = tk.Tk()
#     CountdownApp(root)
#     root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# 
# class CountdownApp:
#     def __init__(self, root):
#         self.root = root
#         self.label = tk.Label(root, text="10", font=("Arial", 60))
#         self.label.pack(expand=True)
#         tk.Button(root, text="시작", command=self.start).pack(pady=10)
# 
#     def start(self):
#         self.count(10)
# 
#     def count(self, i):
#         if i < 0:
#             self.label.config(text="끝!")
#             return
#         self.label.config(text=str(i))
#         self.root.after(1000, self.count, i - 1)
# 
# 
# if __name__ == "__main__":
#     root = tk.Tk()
#     CountdownApp(root)
#     root.mainloop()

# [코드 조각]
# import threading
# import time
# 
# def work():
#     for i in range(5):
#         print(f"작업 중 {i}")
#         time.sleep(1)
# 
# t = threading.Thread(target=work)
# t.start()

# [코드 조각]
# import threading
# import time
# 
# class Worker(threading.Thread):
#     def __init__(self, name):
#         super().__init__()
#         self.worker_name = name
# 
#     def run(self):
#         for i in range(5):
#             print(f"{self.worker_name}: {i}")
#             time.sleep(1)
# 
# w = Worker("작업자1")
# w.start()
