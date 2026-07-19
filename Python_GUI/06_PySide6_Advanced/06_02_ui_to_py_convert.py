# -*- coding: utf-8 -*-
"""
교재 예제 파일: ui 파일 파이썬 코드 변환
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget
from ui_form import Ui_Form

def on_clicked():
    ui.label.setText("실행 되었습니다.")

app = QApplication(sys.argv)

window = QWidget()
ui = Ui_Form()
ui.setupUi(window)

ui.button.clicked.connect(on_clicked)

window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget
# from ui_form import Ui_Form
# 
# app = QApplication(sys.argv)
# 
# window = QWidget()
# ui = Ui_Form()
# ui.setupUi(window)
# 
# window.show()
# sys.exit(app.exec())

# [코드 조각]
# class Ui_Form(object):
#     def setupUi(self, Form):
#         if not Form.objectName():
#             Form.setObjectName(u"Form")
#         Form.resize(168, 93)
#         self.verticalLayout = QVBoxLayout(Form)
#         self.verticalLayout.setObjectName(u"verticalLayout")
#         self.label = QLabel(Form)
#         self.label.setObjectName(u"label")
#         # ... 이하 생략
