# -*- coding: utf-8 -*-
"""
교재 예제 파일: QApplication과 이벤트 루프
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("PySide6 GUI")
window.resize(400, 120)
window.setStyleSheet("background-color: lightblue")

window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget
# 
# app = QApplication(sys.argv)
# window = QWidget()
# window.show()
# sys.exit(app.exec())
