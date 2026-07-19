# -*- coding: utf-8 -*-
"""
교재 예제 파일: 네트워크 점검 스레드 적용
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
from checker import HttpChecker, IcmpChecker, TcpChecker

TYPES = {"HTTP/HTTPS": HttpChecker, "ICMP": IcmpChecker, "TCP": TcpChecker}


class App:
    def __init__(self, root):
        self.root = root
        root.geometry("700x450")

        self.checkers = {}
        self.result_queue = queue.Queue()

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
        self.check_btn = ttk.Button(bottom, text="전체 점검", command=self.check_all)
        self.check_btn.pack(side="left")
        ttk.Button(bottom, text="전체 삭제", command=self.clear).pack(side="left", padx=5)

        self.root.after(100, self.process_queue)

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
        if not self.checkers:
            return

        self.check_btn.config(state="disabled")
        for iid in self.checkers:
            self.tree.set(iid, "result", "점검 중…")
            self.tree.set(iid, "detail", "")
            self.tree.item(iid, tags=())

        targets = list(self.checkers.items())
        thread = threading.Thread(target=self.run_checks, args=(targets,), daemon=True)
        thread.start()

    def run_checks(self, targets):
        for iid, checker in targets:
            try:
                ok, detail = checker.run()
                self.result_queue.put((iid, "정상" if ok else "실패", detail,
                                       "ok" if ok else "fail"))
            except Exception as e:
                self.result_queue.put((iid, "오류", str(e), "fail"))
        self.result_queue.put(("__done__", None, None, None))

    def process_queue(self):
        try:
            while True:
                iid, result, detail, tag = self.result_queue.get_nowait()
                if iid == "__done__":
                    self.check_btn.config(state="normal")
                    continue

                if self.tree.exists(iid):
                    self.tree.set(iid, "result", result)
                    self.tree.set(iid, "detail", detail)
                    self.tree.item(iid, tags=(tag,))
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)

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

# [코드 조각]
# self.result_queue = queue.Queue()

# [코드 조각]
# self.root.after(100, self.process_queue)

# [코드 조각]
# def check_all(self):
#     if not self.checkers:
#         return
# 
#     self.check_btn.config(state="disabled")
#     for iid in self.checkers:
#         self.tree.set(iid, "result", "점검 중…")
#         self.tree.set(iid, "detail", "")
#         self.tree.item(iid, tags=())
# 
#     targets = list(self.checkers.items())
#     thread = threading.Thread(target=self.run_checks, args=(targets,), daemon=True)
#     thread.start()

# [코드 조각]
# def run_checks(self, targets):
#     for iid, checker in targets:
#         try:
#             ok, detail = checker.run()
#             self.result_queue.put((iid, "정상" if ok else "실패", detail,
#                                    "ok" if ok else "fail"))
#         except Exception as e:
#             self.result_queue.put((iid, "오류", str(e), "fail"))
#     self.result_queue.put(("__done__", None, None, None))

# [코드 조각]
# def process_queue(self):
#     try:
#         while True:
#             iid, result, detail, tag = self.result_queue.get_nowait()
#             if iid == "__done__":
#                 self.check_btn.config(state="normal")
#                 continue
#             if self.tree.exists(iid):
#                 self.tree.set(iid, "result", result)
#                 self.tree.set(iid, "detail", detail)
#                 self.tree.item(iid, tags=(tag,))
#     except queue.Empty:
#         pass
#     finally:
#         self.root.after(100, self.process_queue)
