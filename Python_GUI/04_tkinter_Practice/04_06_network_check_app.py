# -*- coding: utf-8 -*-
"""
교재 예제 파일: 네트워크 점검 프로그램
"""

import tkinter as tk
from tkinter import ttk, messagebox
from checker import HttpChecker, IcmpChecker, TcpChecker

TYPES = {"HTTP/HTTPS": HttpChecker, "ICMP": IcmpChecker, "TCP": TcpChecker}


class App:
    def __init__(self, root):
        root.geometry("700x450")

        self.checkers = {}
        top = ttk.Frame(root, padding=10)
        top.pack(fill="x")
        self.type_cb = ttk.Combobox(top, values=list(TYPES), state="readonly", width=12)
        self.type_cb.current(0)
        self.type_cb.pack(side="left")
        self.target_entry = ttk.Entry(top, width=30)
        self.target_entry.pack(side="left", padx=5)
        ttk.Label(top, text="포트:").pack(side="left")
        self.port_entry = ttk.Entry(top, width=8)
        self.port_entry.pack(side="left", padx=(2, 5))
        ttk.Button(top, text="추가", command=self.add).pack(side="left")

        cols = ("type", "target", "result", "detail")
        self.tree = ttk.Treeview(root, columns=cols, show="headings")
        for c, t in zip(cols, ("유형", "대상", "결과", "상세")):
            self.tree.heading(c, text=t)
        self.tree.tag_configure("ok", foreground="green")
        self.tree.tag_configure("fail", foreground="red")
        self.tree.pack(fill="both", expand=True, padx=10)

        bottom = ttk.Frame(root, padding=10)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="전체 점검", command=self.check_all).pack(side="left")
        ttk.Button(bottom, text="전체 삭제", command=self.clear).pack(side="left", padx=5)

    def add(self):
        ctype = self.type_cb.get()
        cls = TYPES[ctype]
        target = self.target_entry.get().strip()
        port = self.port_entry.get().strip()
        if not target:
            messagebox.showwarning("입력 오류", "대상을 입력하세요.")
            return

        if cls is TcpChecker:
            if not port.isdigit():
                messagebox.showwarning("입력 오류", "TCP는 숫자 포트가 필요합니다.")
                return
            checker = cls(target, port)
            shown = f"{target}:{port}"
        else:
            checker = cls(target)
            shown = target

        iid = self.tree.insert("", tk.END, values=(ctype, shown, "-", ""))
        self.checkers[iid] = checker
        self.target_entry.delete(0, tk.END)

    def check_all(self):
        for iid, checker in self.checkers.items():
            try:
                ok, detail = checker.run()
            except Exception as e:
                self.tree.set(iid, "result", "오류")
                self.tree.set(iid, "detail", str(e))
                self.tree.item(iid, tags=("fail",))
                continue

            self.tree.set(iid, "result", "정상" if ok else "실패")
            self.tree.set(iid, "detail", detail)
            self.tree.item(iid, tags=("ok" if ok else "fail",))

    def clear(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        self.checkers.clear()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# from tkinter import ttk, messagebox
# from checker import HttpChecker, IcmpChecker, TcpChecker
# 
# TYPES = {"HTTP/HTTPS": HttpChecker, "ICMP": IcmpChecker, "TCP": TcpChecker}
# 
# 
# class App:
#     def __init__(self, root):
#         root.geometry("560x180")
# 
#         top = ttk.Frame(root, padding=10)
#         top.pack(fill="x")
#         self.type_cb = ttk.Combobox(top, values=list(TYPES), state="readonly", width=12)
#         self.type_cb.current(0)
#         self.type_cb.pack(side="left")
#         self.target_entry = ttk.Entry(top, width=25)
#         self.target_entry.pack(side="left", padx=5)
# 
#         ttk.Label(top, text="포트:").pack(side="left")
#         self.port_entry = ttk.Entry(top, width=8)
#         self.port_entry.pack(side="left", padx=(2, 5))
#         ttk.Button(top, text="점검", command=self.check).pack(side="left")
# 
#         self.result = ttk.Label(root, text="", padding=10, font=("", 12))
#         self.result.pack()
# 
#     def check(self):
#         target = self.target_entry.get().strip()
#         if not target:
#             messagebox.showwarning("입력 오류", "대상을 입력하세요.")
#             return
# 
#         cls = TYPES[self.type_cb.get()]
#         if cls is TcpChecker:
#             port = self.port_entry.get().strip()
#             if not port.isdigit():
#                 messagebox.showwarning("입력 오류", "TCP는 숫자 포트가 필요합니다.")
#                 return
#             checker = cls(target, port)
#         else:
#             checker = cls(target)
# 
#         ok, msg = checker.run()
#         self.result.config(text=f"{'✅' if ok else '❌'} {msg}")
# 
# 
# if __name__ == "__main__":
#     root = tk.Tk()
#     App(root)
#     root.mainloop()

# [코드 조각]
# def add(self):
#     ctype = self.type_cb.get()
#     cls = TYPES[ctype]
#     target = self.target_entry.get().strip()
#     port = self.port_entry.get().strip()

# [코드 조각]
# def check_all(self):
#     for iid, checker in self.checkers.items():

# [코드 조각]
# def clear(self):
#     for iid in self.tree.get_children():
#         self.tree.delete(iid)
#     self.checkers.clear()
