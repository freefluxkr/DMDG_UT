# -*- coding: utf-8 -*-
"""
교재 예제 파일: 세 가지 뷰와 모델
"""

import sys
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem

app = QApplication(sys.argv)

view = QTableView()

model = QStandardItemModel(3, 3)
model.setHorizontalHeaderLabels(["탐사선", "목적지", "현재 상태"])

data = [
    ["보이저 1호", "성간 우주", "통신 양호"],
    ["제임스 웹", "라그랑주 점 (L2)", "심우주 관측 중"],
    ["파커 솔라 프로브", "태양 코로나", "근일점 접근 중"],
]

for row, record in enumerate(data):
    for col, value in enumerate(record):
        item = QStandardItem(value)
        model.setItem(row, col, item)

view.setModel(model)

view.show()

sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QListView
# from PySide6.QtCore import QStringListModel
# 
# app = QApplication(sys.argv)
# 
# view = QListView()
# model = QStringListModel(["☕ 아메리카노", "🥛 카페라떼", "🧋 밀크티"])
# 
# view.setModel(model)
# 
# view.clicked.connect(lambda index: print(f"주문 완료: {index.data()}"))
# 
# view.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QTreeView
# from PySide6.QtGui import QStandardItemModel, QStandardItem
# 
# app = QApplication(sys.argv)
# 
# view = QTreeView()
# 
# model = QStandardItemModel()
# model.setHorizontalHeaderLabels(["조직도"])
# root = model.invisibleRootItem()
# 
# dev_div = QStandardItem("개발본부")
# fe = QStandardItem("프론트엔드")
# fe.appendRow(QStandardItem("이용"))
# 
# be = QStandardItem("백엔드")
# be.appendRow(QStandardItem("김만수"))
# 
# dev_div.appendRow(fe)
# dev_div.appendRow(be)
# 
# root.appendRow(dev_div)
# 
# view.setModel(model)
# view.show()
# 
# sys.exit(app.exec())

# [코드 조각]
# from PySide6.QtWidgets import QAbstractItemView
# 
# view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)       # 읽기 전용
# view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection) # 여러 항목 선택
# view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # 행 단위 선택

# [코드 조각]
# def on_clicked(index):
#     value = view.model().data(index)
#     print(index.row(), index.column(), value)
# 
# view.clicked.connect(on_clicked)

# [코드 조각]
# be = QStandardItem("백엔드")
# be.appendRow(QStandardItem("김만수"))
