# -*- coding: utf-8 -*-
"""
교재 예제 파일: 라벨, 버튼, 입력창
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit

def on_click():
    label.setText(edit.text())
    label.adjustSize()

app = QApplication(sys.argv)
window = QWidget()

label = QLabel("결과", window)
label.move(20, 20)
edit = QLineEdit(window)
edit.move(20, 50)
button = QPushButton("출력", window)
button.move(20, 85)

button.clicked.connect(on_click)

window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QLabel
# from PySide6.QtCore import Qt
# 
# app = QApplication(sys.argv)
# window = QWidget()
# window.resize(300,50)
# 
# label = QLabel("안녕하세요", window)
# label.setText("내용이 바뀌었습니다.")
# label.setAlignment(Qt.AlignmentFlag.AlignCenter)
# label.resize(window.size())
# 
# window.show()
# sys.exit(app.exec())

# [코드 조각]
# from PySide6.QtWidgets import QApplication, QWidget, QLabel
# 
# label = QLabel("안녕하세요", window)

# [코드 조각]
# from PySide6.QtWidgets import QPushButton
# 
# button = QPushButton("확인", window)

# [코드 조각]
# def on_click():
#     print("버튼이 눌렸습니다")
# 
# button = QPushButton("클릭", window)
# button.clicked.connect(on_click)

# [코드 조각]
# from PySide6.QtWidgets import QLineEdit
# 
# edit = QLineEdit(window)
# edit.setPlaceholderText("이름을 입력하세요")
