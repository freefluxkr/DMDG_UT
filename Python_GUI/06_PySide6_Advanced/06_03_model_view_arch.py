# -*- coding: utf-8 -*-
"""
교재 예제 파일: 모델/뷰 아키텍처
"""

import sys
from PySide6.QtWidgets import QApplication, QListView
from PySide6.QtGui import QStandardItemModel, QStandardItem

app = QApplication(sys.argv)

model = QStandardItemModel()
for menu in ["갈비탕", "물냉면", "비빔냉면", "왕만두"]:
    model.appendRow(QStandardItem(menu))

view = QListView()

view.setModel(model)

view.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [코드 조각]
# model.appendRow(QStandardItem(menu))
