# -*- coding: utf-8 -*-
"""
교재 예제 파일: 네트워크 점검 스크립트
"""

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("네트워크 점검 스크립트")
root.geometry("400x300")

label = ttk.Label(root, text="네트워크 점검 스크립트 실습 코드 프레임", font=("Malgun Gothic", 12))
label.pack(pady=20)

root.mainloop()


# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [교재 예제 코드]
# import socket
# import subprocess
# import platform
# import urllib.request
# 
# 
# class Checker:
#     def __init__(self, target):
#         self.target = target
# 
#     def run(self):
#         raise NotImplementedError  # 하위 클래스에서 구현
# 
# 
# class HttpChecker(Checker):
#     def run(self):
#         url = self.target
#         if not url.startswith(("http://", "https://")):
#             url = "http://" + url
#         try:
#             with urllib.request.urlopen(url, timeout=5) as resp:
#                 code = resp.getcode()
#                 return code == 200, f"상태코드 {code}"
#         except Exception as e:
#             return False, f"실패: {e}"
# 
# 
# class IcmpChecker(Checker):
#     def run(self):
#         count = "-n" if platform.system() == "Windows" else "-c"
#         cmd = ["ping", count, "1", self.target]
#         try:
#             result = subprocess.run(cmd, capture_output=True, timeout=5)
#             ok = result.returncode == 0
#             return ok, "응답 성공" if ok else "응답 없음"
#         except Exception as e:
#             return False, f"실패: {e}"
# 
# 
# class TcpChecker(Checker):
#     def __init__(self, target, port):
#         super().__init__(target)
#         self.port = int(port)
# 
#     def run(self):
#         try:
#             with socket.create_connection((self.target, self.port), timeout=5):
#                 return True, "포트 열림"
#         except Exception as e:
#             return False, f"포트 닫힘: {e}"

# [교재 예제 코드]
# def run(self):
#     raise NotImplementedError  # 하위 클래스에서 구현

# [교재 예제 코드]
# cmd = ["ping", count, "1", self.target]

# [교재 예제 코드]
# def __init__(self, target, port):
#     super().__init__(target)
#     self.port = int(port)

# [교재 예제 코드]
# with socket.create_connection((self.target, self.port), timeout=5):
#     return True, "포트 열림"
