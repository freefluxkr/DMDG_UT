# -*- coding: utf-8 -*-
"""
교재 예제 파일: 스타일시트(QSS) 꾸미기
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton
)

app = QApplication(sys.argv)

window = QWidget()

layout = QVBoxLayout()

active_button = QPushButton("마우스를 올려 보세요")
layout.addWidget(active_button)

disabled_button = QPushButton("비활성 버튼")
disabled_button.setEnabled(False)
layout.addWidget(disabled_button)

window.setLayout(layout)

window.setStyleSheet("""
    QPushButton {
        background-color: #3498db;
        color: white;
        font-size: 14px;
        padding: 8px;
        border: none;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #5dade2;
    }
    QPushButton:pressed {
        background-color: #2e86c1;
    }
    QPushButton:disabled {
        background-color: #bdc3c7;
    }
""")

window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QPushButton
# 
# app = QApplication(sys.argv)
# 
# button = QPushButton("스타일 버튼")
# button.setStyleSheet("""
#     background-color: #3498db;
#     color: white;
#     font-size: 20px;
#     padding: 7px;
# """)
# 
# button.show()
# 
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout,
#     QLabel, QLineEdit, QPushButton
# )
# 
# app = QApplication(sys.argv)
# 
# window = QWidget()
# layout = QVBoxLayout()
# layout.addWidget(QLabel("이름"))
# layout.addWidget(QLineEdit())
# layout.addWidget(QPushButton("확인"))
# window.setLayout(layout)
# 
# window.setStyleSheet("""
#     QWidget {
#         background-color: #2c3e50;
#     }
#     QLabel {
#         color: #ecf0f1;
#         font-size: 14px;
#     }
#     QLineEdit {
#         background-color: white;
#         border: 1px solid #bdc3c7;
#         border-radius: 4px;
#         padding: 6px;
#     }
#     QPushButton {
#         background-color: #e74c3c;
#         color: white;
#         padding: 8px;
#         border-radius: 4px;
#     }
# """)
# 
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QPushButton
# 
# app = QApplication(sys.argv)
# 
# with open("style.qss", "r", encoding="utf-8") as f:
#     app.setStyleSheet(f.read())
# 
# button = QPushButton("테마 적용 버튼")
# button.show()
# 
# sys.exit(app.exec())

# [코드 조각]
# QPushButton {
#     background-color: #3498db;
#     color: white;
# }

# [코드 조각]
# app.setStyleSheet("QPushButton { color: red; }")   # 앱 전체 버튼
# window.setStyleSheet("QPushButton { color: red; }") # 이 창 안의 버튼
# button.setStyleSheet("color: red;")                 # 이 버튼 하나

# [코드 조각]
# ok_button = QPushButton("확인")
# ok_button.setObjectName("okButton")   # 이름 지정
# 
# window.setStyleSheet("""
#     QPushButton {
#         background-color: gray;       /* 모든 버튼 */
#     }
#     QPushButton#okButton {
#         background-color: #27ae60;    /* 이름이 okButton인 버튼만 */
#     }
# """)

# [코드 조각]
# QCheckBox::indicator {
#     width: 18px;
#     height: 18px;
# }
# QComboBox::drop-down {
#     border: none;
# }

# [코드 조각]
# /* style.qss */
# QWidget {
#     background-color: #2c3e50;
# }
# QPushButton {
#     background-color: #e74c3c;
#     color: white;
#     padding: 8px;
#     border-radius: 4px;
# }
# QPushButton:hover {
#     background-color: #ec7063;
# }
