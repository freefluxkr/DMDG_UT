# -*- coding: utf-8 -*-
"""
교재 예제 파일: 시그널과 슬롯
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Signal

class Counter(QWidget):
    countChanged = Signal(int)          # 1. 정의: 정수로 시그널 정의

    def __init__(self):
        super().__init__()
        self.count = 0
        label = QLabel("0")             
        button = QPushButton("증가")
        button.clicked.connect(self.increase)
        self.countChanged.connect(label.setNum) # 2. 연결: countChanged 신호가 오면 라벨에 숫자 표시

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(button)

    def increase(self):
        self.count += 1
        self.countChanged.emit(self.count) # 3. 발생: 값이 바뀔 때마다 변경된 숫자를 담아 발송

app = QApplication(sys.argv)
window = Counter()
window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
# 
# app = QApplication(sys.argv)
# window = QWidget()
# 
# layout = QVBoxLayout(window)
# button = QPushButton("닫기")
# 
# button.clicked.connect(window.close)
# 
# layout.addWidget(button)
# window.show()
# 
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout
# )
# 
# app = QApplication(sys.argv)
# window = QWidget()
# 
# edit = QLineEdit()
# label = QLabel("여기에 표시됩니다.")
# 
# edit.textChanged.connect(label.setText)
# 
# layout = QVBoxLayout()
# layout.addWidget(edit)
# layout.addWidget(label)
# window.setLayout(layout)
# 
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QProgressBar
# from PySide6.QtCore import Qt
# 
# app = QApplication(sys.argv)
# window = QWidget()
# layout = QVBoxLayout(window)
# 
# slider = QSlider(Qt.Horizontal)
# progress_bar = QProgressBar()
# 
# slider.valueChanged.connect(progress_bar.setValue)
# 
# layout.addWidget(slider)
# layout.addWidget(progress_bar)
# window.show()
# 
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
# )
# 
# def on_click(what):
#     label.setText(f"{what} 버튼을 눌렀습니다.")
# 
# app = QApplication(sys.argv)
# window = QWidget()
# 
# label = QLabel("버튼을 눌러보세요.")
# layout = QVBoxLayout()
# layout.addWidget(label)
# 
# buttons = [("Start", "출발"), ("Stop", "정지"), ("Pause", "일시정지")]
# 
# for text, message in buttons:
#     button = QPushButton(text)
#     button.clicked.connect(lambda checked=False, message=message: on_click(message))
#     layout.addWidget(button)
# 
# window.setLayout(layout)
# window.show()
# sys.exit(app.exec())

# [코드 조각]
# 시그널이름 = Signal(int)       # 1. 정의 (int 값을 전달하겠다고 선언)
# ...
# self.시그널이름.connect(슬롯)  # 2. 연결 (신호가 오면 슬롯 실행)
# ...
# self.시그널이름.emit(현재값)   # 3. 발생 (원하는 순간에 값을 담아 발송)

# [코드 조각]
# statusChanged = Signal(str, int)   # 문자열과 정수를 함께 전달
# ...
# self.statusChanged.emit("완료", 100)   # 두 값을 함께 emit
