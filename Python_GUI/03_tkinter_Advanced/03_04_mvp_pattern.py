# -*- coding: utf-8 -*-
"""
교재 예제 파일: MVP 패턴 적용
"""

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("MVP 패턴 적용")
root.geometry("400x300")

label = ttk.Label(root, text="MVP 패턴 적용 실습 코드 프레임", font=("Malgun Gothic", 12))
label.pack(pady=20)

root.mainloop()


# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [교재 예제 코드]
# class DistanceModel:
#     KM_PER_MILE = 1.609344
# 
#     def km_to_miles(self, km):
#         return km / self.KM_PER_MILE
# 
#     def miles_to_km(self, miles):
#         return miles * self.KM_PER_MILE

# [교재 예제 코드]
# import tkinter as tk
# 
# 
# class DistanceView(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.pack(padx=15, pady=15)
# 
#         self.entry = tk.Entry(self, width=15)
#         self.entry.grid(row=0, column=0, columnspan=2, pady=5)
# 
#         self.km_btn = tk.Button(self, text="km → 마일")
#         self.km_btn.grid(row=1, column=0, padx=2)
# 
#         self.mile_btn = tk.Button(self, text="마일 → km")
#         self.mile_btn.grid(row=1, column=1, padx=2)
# 
#         self.result = tk.Label(self, text="값을 입력하세요", width=25)
#         self.result.grid(row=2, column=0, columnspan=2, pady=10)
# 
#     def get_input(self):
#         return self.entry.get()
# 
#     def show_result(self, text):
#         self.result.config(text=text)

# [교재 예제 코드]
# class DistancePresenter:
#     def __init__(self, model, view):
#         self.model = model
#         self.view = view
# 
#         self.view.km_btn.config(command=self.on_km_to_miles)
#         self.view.mile_btn.config(command=self.on_miles_to_km)
# 
#     def _read_value(self):
#         """입력값을 숫자로 변환. 실패하면 None과 함께 안내."""
#         try:
#             return float(self.view.get_input())
#         except ValueError:
#             self.view.show_result("숫자를 입력하세요")
#             return None
# 
#     def on_km_to_miles(self):
#         value = self._read_value()
#         if value is not None:
#             miles = self.model.km_to_miles(value)
#             self.view.show_result(f"{value} km = {miles:.2f} 마일")
# 
#     def on_miles_to_km(self):
#         value = self._read_value()
#         if value is not None:
#             km = self.model.miles_to_km(value)
#             self.view.show_result(f"{value} 마일 = {km:.2f} km")

# [교재 예제 코드]
# if __name__ == "__main__":
#     root = tk.Tk()
#     presenter = DistancePresenter(DistanceModel(), DistanceView(root))
#     root.mainloop()

# [교재 예제 코드]
# def __init__(self, model, view):
#     #                ↑ 첫 번째 인자가  ↑ 두 번째 인자가
#     #                  model에 들어옴   view에 들어옴
#     self.model = model
#     self.view = view
