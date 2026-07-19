# -*- coding: utf-8 -*-
"""
교재 예제 파일: 위젯 개념과 계층 구조
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton

app = QApplication(sys.argv)

window = QWidget()
window.resize(300, 120)

label = QLabel("이름을 입력하세요", window)
label.move(20, 20)

button = QPushButton("확인", window)
button.move(20, 60)

window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QPushButton
# 
# app = QApplication(sys.argv)
# 
# window = QWidget()
# window.resize(300, 200)
# 
# button = QPushButton("자식 위젯", window)
# button.move(80, 80)
# 
# window.show()
# sys.exit(app.exec())

# [코드 조각]
# from PySide6.QtWidgets import QWidget, QPushButton, QLabel
# 
# button = QPushButton("확인")
# label = QLabel("안녕하세요")
# button.resize(100, 40)
# label.move(10, 10)

# [코드 조각]
# QWidget (최상위 창)
# ├── QLabel        "제목"
# ├── QPushButton   "확인"
# └── QWidget       (영역을 묶는 컨테이너)
#     ├── QLineEdit  입력창
#     └── QPushButton "전송"
