# -*- coding: utf-8 -*-
"""
교재 예제 파일: 그래픽 뷰 프레임워크
"""

import sys
from PySide6.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView, 
                               QGraphicsRectItem, QGraphicsItem)
from PySide6.QtGui import QBrush, QColor


class ColorBox(QGraphicsRectItem):
    def __init__(self, x, y):
        super().__init__(0, 0, 80, 80)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("skyblue")))

        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable) 

    def mousePressEvent(self, event):
        new_color = "orange" if self.brush().color() == QColor("skyblue") else "skyblue"
        self.setBrush(QBrush(QColor(new_color)))
        super().mousePressEvent(event)


class ZoomView(QGraphicsView):
    def wheelEvent(self, event):
        self.scale(1.1, 1.1) if event.angleDelta().y() > 0 else self.scale(0.9, 0.9)


app = QApplication(sys.argv)
scene = QGraphicsScene(0, 0, 400, 300)

scene.addItem(ColorBox(50, 50))
scene.addItem(ColorBox(200, 150))

view = ZoomView(scene)
view.resize(450, 350)
view.show()

sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
# 
# app = QApplication(sys.argv)
# 
# scene = QGraphicsScene()
# scene.setSceneRect(0, 0, 400, 300)
# 
# view = QGraphicsView(scene)
# view.show()
# 
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
# from PySide6.QtGui import QPen, QBrush
# from PySide6.QtCore import Qt
# 
# app = QApplication(sys.argv)
# 
# scene = QGraphicsScene()
# scene.setSceneRect(0, 0, 400, 180)
# 
# ellipse = scene.addEllipse(40, 30, 90, 90, QPen(Qt.red), QBrush(Qt.yellow))
# 
# view = QGraphicsView(scene)
# view.show()
# 
# sys.exit(app.exec())

# [코드 조각]
# from PySide6.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView, 
#                                QGraphicsRectItem, QGraphicsItem)

# [코드 조각]
# class ColorBox(QGraphicsRectItem):

# [코드 조각]
# def __init__(self, x, y):
#         super().__init__(0, 0, 80, 80)

# [코드 조각]
# def mousePressEvent(self, event):
#         new_color = "orange" if self.brush().color() == QColor("skyblue") else "skyblue"
#         self.setBrush(QBrush(QColor(new_color)))
#         super().mousePressEvent(event)

# [코드 조각]
# def wheelEvent(self, event):
#         self.scale(1.1, 1.1) if event.angleDelta().y() > 0 else self.scale(0.9, 0.9)

# [코드 조각]
# scene = QGraphicsScene(0, 0, 400, 300)
