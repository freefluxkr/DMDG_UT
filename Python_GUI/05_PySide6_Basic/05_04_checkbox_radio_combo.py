# -*- coding: utf-8 -*-
"""
교재 예제 파일: 체크박스, 라디오, 콤보박스
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QRadioButton

app = QApplication(sys.argv)
window = QWidget()

radio1 = QRadioButton("남성", window)
radio1.move(20, 20)
radio2 = QRadioButton("여성", window)
radio2.move(50, 20)
radio1.setChecked(True)

window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QCheckBox
# 
# app = QApplication(sys.argv)
# window = QWidget()
# 
# check = QCheckBox("앱 푸시 동의", window)
# check.setChecked(True)
# check.move(20, 20)
# 
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QComboBox
# 
# app = QApplication(sys.argv)
# window = QWidget()
# 
# combo = QComboBox(window)
# combo.addItems(["대중교통", "자가용", "도보"])
# combo.setCurrentIndex(1)
# combo.move(20, 20)
# 
# window.show()
# sys.exit(app.exec())

# [코드 조각]
# from PySide6.QtWidgets import QApplication, QWidget, QCheckBox
# 
# check = QCheckBox("앱 푸시 동의", window)

# [코드 조각]
# from PySide6.QtWidgets import QRadioButton
# 
# radio = QRadioButton("남성", window)

# [코드 조각]
# from PySide6.QtWidgets import QComboBox
# 
# combo = QComboBox(window)
# combo.addItems(["대중교통", "자가용", "도보"])
