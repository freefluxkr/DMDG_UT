# -*- coding: utf-8 -*-
"""
교재 예제 파일: 슬라이더와 프로그레스바
"""

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QSlider

app = QApplication(sys.argv)
window = QWidget()

slider = QSlider(Qt.Horizontal, window)
slider.setRange(0, 100)
slider.setValue(30)
slider.move(20, 20)
slider.resize(200, 20)

window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QSpinBox
# 
# app = QApplication(sys.argv)
# window = QWidget()
# 
# spin = QSpinBox(window)
# spin.setRange(0, 12)
# spin.setSuffix(" 개")
# spin.move(20, 20)
# 
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QProgressBar
# 
# app = QApplication(sys.argv)
# window = QWidget()
# 
# bar = QProgressBar(window)
# bar.setRange(0, 100)
# bar.setValue(37)
# bar.move(20, 20)
# bar.resize(200, 25)
# 
# window.show()
# sys.exit(app.exec())

# [코드 조각]
# from PySide6.QtCore import Qt
# from PySide6.QtWidgets import QApplication, QWidget, QSlider
# 
# slider = QSlider(Qt.Horizontal, window)

# [코드 조각]
# from PySide6.QtWidgets import QSpinBox
# 
# spin = QSpinBox(window)
# spin.setRange(0, 12)

# [코드 조각]
# from PySide6.QtWidgets import QProgressBar
# 
# bar = QProgressBar(window)
# bar.setValue(37)
