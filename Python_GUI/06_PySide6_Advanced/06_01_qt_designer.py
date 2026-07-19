# -*- coding: utf-8 -*-
"""
교재 예제 파일: Qt Designer 활용
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

app = QApplication(sys.argv)

loader = QUiLoader()
ui_file = QFile("form.ui")
ui_file.open(QFile.OpenModeFlag.ReadOnly)
window = loader.load(ui_file)
ui_file.close()

def on_clicked():
    window.label.setText("실행 되었습니다.")

window.button.clicked.connect(on_clicked)

window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [코드 조각]
# ~ 생략 ~
# <item>
#  <widget class="QLabel" name="label">
#   <property name="text">
#    <string>결과값 출력 위치입니다</string>
#   </property>
#  </widget>
# </item>
# <item>
#  <widget class="QPushButton" name="button">
#   <property name="text">
#    <string>실행</string>
#   </property>
#  </widget>
# </item>
# ~ 생략 ~

# [코드 조각]
# ui_file.open(QFile.OpenModeFlag.ReadOnly)
