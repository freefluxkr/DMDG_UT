# -*- coding: utf-8 -*-
"""
교재 예제 파일: OOP 기반 GUI 구조 설계
"""

import tkinter as tk


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x350")
        self.total_count = 0
        self.done_count = 0

        self._create_widgets()
        self.update_status()

    def _create_widgets(self):
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=(0, 7))

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill="x", padx=10, pady=10)

        self.status_label = tk.Label(self.root)
        self.status_label.pack()

        buttons = [
            ("추가", self.add_item),
            ("완료 처리", self.mark_done),
            ("삭제", self.delete_item),
            ("전체 비우기", self.clear_all),
        ]
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command).pack()

    def update_status(self):
        self.status_label.config(
            text=f"전체 {self.total_count}개 / 완료 {self.done_count}개"
        )

    def add_item(self):
        text = self.entry.get().strip()
        if text:
            self.listbox.insert(tk.END, text)
            self.entry.delete(0, tk.END)
            self.total_count += 1
            self.update_status()

    def delete_item(self):
        selected = self.listbox.curselection()
        if selected:
            self.listbox.delete(selected[0])
            self.total_count -= 1
            self.update_status()

    def mark_done(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            text = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index, "[완료] " + text)
            self.done_count += 1
            self.update_status()

    def clear_all(self):
        self.listbox.delete(0, tk.END)
        self.total_count = 0
        self.done_count = 0
        self.update_status()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# 
# class Application(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("300x80")
#         self.label = tk.Label(self, text="안녕하세요")
#         self.label.pack(pady=5)
#         tk.Button(self, text="클릭", command=self.on_click).pack()
# 
#     def on_click(self):
#         self.label.config(text="버튼을 눌렀습니다")
# 
# 
# if __name__ == "__main__":
#     Application().mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# class CounterFrame(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.count = 0
#         self.display = tk.Label(self, text="0", font=("맑은 고딕", 24))
#         self.display.pack(pady=10)
#         tk.Button(self, text="+1", command=self.increase).pack()
# 
#     def increase(self):
#         self.count += 1
#         self.display.config(text=str(self.count))
# 
# 
# if __name__ == "__main__":
#     root = tk.Tk()
#     CounterFrame(root).pack(padx=20, pady=20)
#     root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# class NameInput(tk.Frame):
#     def __init__(self, master, on_submit):
#         super().__init__(master)
#         self.on_submit = on_submit
#         self.entry = tk.Entry(self)
#         self.entry.pack(side="left")
#         tk.Button(self, text="인사하기", command=self.submit).pack(side="left")
# 
#     def submit(self):
#         self.on_submit(self.entry.get())
# 
# 
# class Greeting(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.label = tk.Label(self, text="", font=("맑은 고딕", 14))
#         self.label.pack()
# 
#     def show(self, name):
#         self.label.config(text=f"안녕하세요, {name}님!")
# 
# 
# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("300x120")
#         self.greeting = Greeting(self)
#         self.name_input = NameInput(self, on_submit=self.greeting.show)
#         self.name_input.pack(pady=10)
#         self.greeting.pack(pady=10)
# 
# 
# if __name__ == "__main__":
#     App().mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# class PageOne(tk.Frame):
#     def __init__(self, master, controller):
#         super().__init__(master)
#         tk.Label(self, text="첫 번째 페이지", font=("맑은 고딕", 16)).pack(pady=20)
#         tk.Button(self, text="다음으로",
#                   command=lambda: controller.show_page("PageTwo")).pack()
# 
# 
# class PageTwo(tk.Frame):
#     def __init__(self, master, controller):
#         super().__init__(master)
#         tk.Label(self, text="두 번째 페이지", font=("맑은 고딕", 16)).pack(pady=20)
#         tk.Button(self, text="이전으로",
#                   command=lambda: controller.show_page("PageOne")).pack()
# 
# 
# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("300x200")
#         self.pages = {}
#         for PageClass in (PageOne, PageTwo):
#             page = PageClass(self, self)
#             self.pages[PageClass.__name__] = page
#             page.grid(row=0, column=0, sticky="nsew")
#         self.show_page("PageOne")
# 
#     def show_page(self, name):
#         self.pages[name].tkraise()
# 
# 
# if __name__ == "__main__":
#     App().mainloop()

# [코드 조각]
# self.display = tk.Label(self, text="0", font=("맑은 고딕", 24))

# [코드 조각]
# self.name_input = NameInput(self, on_submit=self.greeting.show)

# [코드 조각]
# for PageClass in (PageOne, PageTwo):
#     page = PageClass(self, self)
#     self.pages[PageClass.__name__] = page
#     page.grid(row=0, column=0, sticky="nsew")

# [코드 조각]
# def show_page(self, name):
#     self.pages[name].tkraise()
