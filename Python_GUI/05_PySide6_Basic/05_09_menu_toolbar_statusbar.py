# -*- coding: utf-8 -*-
"""
교재 예제 파일: 메뉴, 툴바, 상태바
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtGui import QAction

app = QApplication(sys.argv)

window = QMainWindow()
window.resize(400, 300)

editor = QTextEdit()
window.setCentralWidget(editor)

open_action = QAction("열기", window)
open_action.setShortcut("Ctrl+O")
open_action.triggered.connect(lambda: window.statusBar().showMessage("열기 실행됨!", 3000))

exit_action = QAction("종료", window)
exit_action.triggered.connect(app.quit)

file_menu = window.menuBar().addMenu("파일")
file_menu.addAction(open_action)
file_menu.addSeparator()
file_menu.addAction(exit_action)

toolbar = window.addToolBar("기본 툴바")
toolbar.addAction(open_action)
toolbar.addAction(exit_action)

window.statusBar().showMessage("이곳이 상태바")

window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
# 
# app = QApplication(sys.argv)
# 
# window = QMainWindow()
# 
# editor = QTextEdit()
# window.setCentralWidget(editor)
# 
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow
# from PySide6.QtGui import QAction
# 
# app = QApplication(sys.argv)
# 
# window = QMainWindow()
# 
# exit_action = QAction("종료", window)
# exit_action.triggered.connect(app.quit)
# 
# file_menu = window.menuBar().addMenu("파일")
# file_menu.addAction(exit_action)
# 
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow
# from PySide6.QtGui import QAction
# 
# app = QApplication(sys.argv)
# 
# window = QMainWindow()
# 
# exit_action = QAction("종료", window)
# exit_action.triggered.connect(app.quit)
# 
# toolbar = window.addToolBar("기본 툴바")
# toolbar.addAction(exit_action)
# 
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow
# 
# app = QApplication(sys.argv)
# 
# window = QMainWindow()
# window.statusBar().showMessage("이곳이 상태바")
# 
# window.show()
# sys.exit(app.exec())

# [코드 조각]
# from PySide6.QtGui import QAction
# 
# open_action = QAction("열기", window)
# open_action.triggered.connect(some_func)
