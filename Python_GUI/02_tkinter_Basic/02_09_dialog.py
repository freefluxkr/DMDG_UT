# -*- coding: utf-8 -*-
"""
교재 예제 파일: 대화상자 (Dialog)
"""

import tkinter as tk

root = tk.Tk()
root.title("메인 창")
root.geometry("300x100")

result = tk.Label(root, text="결과 : 없음")
result.pack(pady=10)

def ask_name():
    dialog = tk.Toplevel(root)
    dialog.title("이름 입력")

    tk.Label(dialog, text="이름을 입력해 주세요!").pack(pady=5)
    entry = tk.Entry(dialog)
    entry.pack(padx=20)

    def confirm():
        result.config(text=f"결과 : {entry.get()}")
        dialog.destroy()

    tk.Button(dialog, text="확인", command=confirm).pack(pady=10)

    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

tk.Button(root, text="입력 받기", command=ask_name).pack()
root.mainloop()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import tkinter as tk
# from tkinter import messagebox
# 
# root = tk.Tk()
# 
# def exit_app():
#     if messagebox.askyesno("확인", "정말 종료할까요?"):
#         root.destroy()
# 
# tk.Button(root, text="종료", command=exit_app).pack(padx=180, pady=48)
# root.mainloop()

# [다른 예제 코드]
# import tkinter as tk
# 
# root = tk.Tk()
# root.title("메인 창")
# root.geometry("300x200")
# 
# def open_window():
#     win = tk.Toplevel(root)             # 새 창 생성
#     win.title("새 창")
#     tk.Label(win, text="이건 새 창입니다!").pack(pady=20)
#     tk.Button(win, text="닫기", command=win.destroy).pack()
# 
# tk.Button(root, text="새 창 열기", command=open_window).pack(pady=50)
# root.mainloop()
