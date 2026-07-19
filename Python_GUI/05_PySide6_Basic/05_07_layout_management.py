# -*- coding: utf-8 -*-
"""
교재 예제 파일: 레이아웃 관리
"""

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel

app = QApplication([])
window = QWidget()

main = QVBoxLayout(window)

top = QLabel("상단")
top.setStyleSheet("background:#e74c3c; padding:15px;")
main.addWidget(top)

middle = QHBoxLayout()

left = QLabel("좌")
left.setStyleSheet("background:#3498db; padding:15px;")
right = QLabel("우")
right.setStyleSheet("background:#f39c12; padding:15px;")

middle.addWidget(left)
middle.addWidget(right)
main.addLayout(middle)

bottom = QLabel("하단")
bottom.setStyleSheet("background:#9b59b6; padding:15px;")
main.addWidget(bottom)

window.show()
app.exec()

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# 
# app = QApplication(sys.argv)
# window = QWidget()
# layout = QVBoxLayout()
# 
# layout.addWidget(QLabel("첫 번째", styleSheet="padding:20px; background:#e74c3c"))
# layout.addWidget(QLabel("두 번째", styleSheet="padding:20px; background:#2ecc71"))
# layout.addWidget(QLabel("세 번째", styleSheet="padding:20px; background:#3498db"))
# 
# window.setLayout(layout)
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout
# 
# app = QApplication(sys.argv)
# window = QWidget()
# layout = QHBoxLayout()
# 
# layout.addWidget(QPushButton("이전", styleSheet="background:#95a5a6; padding:15px"))
# layout.addWidget(QPushButton("확인", styleSheet="background:#3498db; padding:15px"))
# layout.addWidget(QPushButton("다음", styleSheet="background:#95a5a6; padding:15px"))
# 
# window.setLayout(layout)
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
# 
# app = QApplication(sys.argv)
# window = QWidget()
# layout = QGridLayout()
# 
# style = "color:white; padding:20px; font-size:16px; background:"
# layout.addWidget(QLabel("0,0", styleSheet=style + "#e74c3c"), 0, 0)
# layout.addWidget(QLabel("0,1", styleSheet=style + "#2ecc71"), 0, 1)
# layout.addWidget(QLabel("1,0", styleSheet=style + "#3498db"), 1, 0)
# layout.addWidget(QLabel("1,1", styleSheet=style + "#f39c12"), 1, 1)
# 
# window.setLayout(layout)
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QLineEdit, QFormLayout
# )
# 
# app = QApplication(sys.argv)
# window = QWidget()
# layout = QFormLayout()
# 
# layout.addRow("이름", QLineEdit())
# layout.addRow("이메일", QLineEdit())
# layout.addRow("설명", QLineEdit())
# 
# window.setLayout(layout)
# window.show()
# sys.exit(app.exec())

# [코드 조각]
# layout = QVBoxLayout()
# layout.addWidget(button)
# window.setLayout(layout)

# [코드 조각]
# layout = QHBoxLayout()
# 
# layout.addStretch()
# layout.addWidget(QPushButton("이전", styleSheet="background:#95a5a6; padding:15px"))

# [코드 조각]
# layout.addWidget(QLabel("0,0~1", styleSheet=style + "#e74c3c"), 0, 0, 1, 2)
