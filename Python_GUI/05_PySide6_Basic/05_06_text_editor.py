# -*- coding: utf-8 -*-
"""
교재 예제 파일: 텍스트 편집기
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QTextEdit, QTextBrowser, QPushButton

app = QApplication(sys.argv)
window = QWidget()
layout = QHBoxLayout()

editor = QTextEdit("이곳에 텍스트 입력합니다.")
result = QTextBrowser()

def read_write():
    result.setHtml(editor.toPlainText())

button = QPushButton("옮기기")
button.clicked.connect(read_write)

layout.addWidget(editor)
layout.addWidget(button)
layout.addWidget(result)

window.setLayout(layout)
window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [코드 조각]
# from PySide6.QtWidgets import QApplication, QWidget, QTextEdit
# 
# editor = QTextEdit("이곳에 텍스트 입력합니다.")

# [코드 조각]
# from PySide6.QtWidgets import QApplication, QPlainTextEdit
# 
# app = QApplication([])
# 
# log = QPlainTextEdit()
# log.appendPlainText("프로그램을 시작했습니다")
# print(log.toPlainText())
