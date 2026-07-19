# -*- coding: utf-8 -*-
"""
교재 예제 파일: MVP 패턴 연락처 앱
"""

import tkinter as tk

from model import ContactModel
from view import ContactView
from presenter import ContactPresenter


def main():
    root = tk.Tk()
    root.title("연락처 v0.3")

    view = ContactView(root)
    model = ContactModel()
    ContactPresenter(view, model)

    root.mainloop()


if __name__ == "__main__":
    main()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [코드 조각]
# import os, json
# 
# 
# class ContactModel:
#     def __init__(self, file_path="contacts.json"):
#         self.file_path = file_path
#         self.contacts = self._load()
# 
#     def _load(self):
#         if os.path.exists(self.file_path):
#             with open(self.file_path, encoding="utf-8") as f:
#                 return json.load(f)
#         return []
# 
#     def _save(self):
#         with open(self.file_path, "w", encoding="utf-8") as f:
#             json.dump(self.contacts, f, ensure_ascii=False, indent=2)
# 
#     def get_all(self):
#         return self.contacts
# 
#     def add(self, name, company, phone):
#         self.contacts.append({"name": name, "company": company, "phone": phone})
#         self._save()
# 
#     def delete(self, idx):
#         self.contacts.pop(idx)
#         self._save()

# [코드 조각]
# import tkinter as tk
# from tkinter import ttk, messagebox
# 
# 
# class ContactView:
#     def __init__(self, root):
#         self.root = root
#         self.presenter = None
#         self._setup_ui()
# 
#     def set_presenter(self, presenter):
#         self.presenter = presenter
# 
#     def _setup_ui(self):
#         input_frame = tk.LabelFrame(self.root, text="입력", padx=10, pady=10)
#         input_frame.pack(padx=10, pady=10, fill="x")
# 
#         tk.Label(input_frame, text="이름").grid(row=0, column=0)
#         tk.Label(input_frame, text="회사").grid(row=0, column=1)
#         tk.Label(input_frame, text="전화").grid(row=0, column=2)
# 
#         self.e_name = tk.Entry(input_frame)
#         self.e_company = tk.Entry(input_frame)
#         self.e_phone = tk.Entry(input_frame)
# 
#         self.e_name.grid(row=1, column=0, padx=2)
#         self.e_company.grid(row=1, column=1, padx=2)
#         self.e_phone.grid(row=1, column=2, padx=2)
# 
#         tk.Button(input_frame, text="추가",
#                   command=lambda: self.presenter.add()).grid(row=1, column=3, padx=5)
#         tk.Button(input_frame, text="삭제",
#                   command=lambda: self.presenter.delete()).grid(row=1, column=4)
# 
#         list_frame = tk.LabelFrame(self.root, text="목록", padx=10, pady=10)
#         list_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)
# 
#         self.tree = ttk.Treeview(list_frame, columns=("name", "company", "phone"),
#                                  show="headings", height=8)
#         self.tree.heading("name", text="이름")
#         self.tree.heading("company", text="회사")
#         self.tree.heading("phone", text="전화")
#         self.tree.pack(fill="both", expand=True)
# 
#     def get_inputs(self):
#         return self.e_name.get(), self.e_company.get(), self.e_phone.get()
# 
#     def clear_inputs(self):
#         for e in (self.e_name, self.e_company, self.e_phone):
#             e.delete(0, "end")
# 
#     def get_selected_index(self):
#         sel = self.tree.selection()
#         if not sel:
#             return None
#         return self.tree.index(sel[0])
# 
#     def render(self, contacts):
#         self.tree.delete(*self.tree.get_children())
#         for c in contacts:
#             self.tree.insert("", "end", values=(c["name"], c["company"], c["phone"]))
# 
#     def show_warning(self, title, message):
#         messagebox.showwarning(title, message)

# [코드 조각]
# if __name__ == "__main__":
#     root = tk.Tk()
#     view = ContactView(root)
#     root.mainloop()

# [코드 조각]
# class ContactPresenter:
#     def __init__(self, view, model):
#         self.view = view
#         self.model = model
#         self.view.set_presenter(self)
#         self.refresh()
# 
#     def refresh(self):
#         self.view.render(self.model.get_all())
# 
#     def add(self):
#         name, company, phone = self.view.get_inputs()
#         if not name:
#             self.view.show_warning("확인", "이름을 입력하세요.")
#             return
#         self.model.add(name, company, phone)
#         self.refresh()
#         self.view.clear_inputs()
# 
#     def delete(self):
#         idx = self.view.get_selected_index()
#         if idx is None:
#             return
#         self.model.delete(idx)
#         self.refresh()
