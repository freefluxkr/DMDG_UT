# -*- coding: utf-8 -*-
"""
교재 예제 파일: 대화상자 (QDialog)
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout(window)

btn_file = QPushButton("파일 열기")
btn_folder = QPushButton("폴더 선택")
layout.addWidget(btn_file)
layout.addWidget(btn_folder)

btn_file.clicked.connect(lambda: print("선택한 파일:", QFileDialog.getOpenFileName(window, "파일 열기", "", "텍스트 파일 (*.txt);;모든 파일 (*)")[0]))
btn_folder.clicked.connect(lambda: print("선택한 폴더:", QFileDialog.getExistingDirectory(window, "폴더 선택")))

window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
# 
# app = QApplication(sys.argv)
# window = QWidget()
# 
# def show_message():
#     QMessageBox.warning(window, "경고", "이 작업은 CPU 사용률이 매우 높습니다.")
# 
# button = QPushButton("주의", window)
# button.clicked.connect(show_message)
# button.move(80, 80)
# 
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# from PySide6.QtWidgets import QApplication, QLabel, QFontDialog
# 
# app = QApplication(sys.argv)
# 
# label = QLabel("폰트 선택 대화상자")
# 
# ok, font = QFontDialog.getFont()
# if ok:
#     label.setFont(font)
#     print("선택한 폰트:", font.family(), font.pointSize())
# 
# label.show()
# sys.exit(app.exec())

# [코드 조각]
# reply = QMessageBox.question(
#     window, "확인",
#     "정말 삭제하시겠습니까?",
#     QMessageBox.Yes | QMessageBox.No
# )
# 
# if reply == QMessageBox.Yes:
#     print("삭제 진행")
# else:
#     print("취소됨")

# [코드 조각]
# from PySide6.QtWidgets import QApplication, QWidget, QInputDialog
# 
# app = QApplication([])
# window = QWidget()
# 
# text, ok = QInputDialog.getText(window, "이름 입력", "이름을 입력하세요:")
# if ok and text: 
#     print("이름: ", text)
# 
# num, ok = QInputDialog.getInt(window, "나이 입력", "나이:", 20, 0, 120)
# if ok: 
#     print("나이: ", num)
# 
# genders = ["남자", "여자"]
# gender, ok = QInputDialog.getItem(window, "성별 입력", "성별을 선택하세요:", genders, 0, False)
# if ok and gender: 
#     print("성별: ", gender)

# [코드 조각]
# import sys
# from PySide6.QtWidgets import QApplication, QColorDialog
# 
# app = QApplication(sys.argv)
# 
# color = QColorDialog.getColor()
# if color.isValid():
#     print("선택한 색:", color.name())

# [코드 조각]
# import sys
# from PySide6.QtWidgets import (
#     QApplication, QDialog, QVBoxLayout, QLabel,
#     QLineEdit, QComboBox, QRadioButton, QButtonGroup, QDialogButtonBox
# )
# 
# def create_profile_dialog(parent=None):
#     dialog = QDialog(parent)
#     dialog.setWindowTitle("사용자 프로필")
#     layout = QVBoxLayout()
# 
#     layout.addWidget(QLabel("닉네임:"))
#     nick = QLineEdit()
#     layout.addWidget(nick)
# 
#     layout.addWidget(QLabel("직업:"))
#     job = QComboBox()
#     job.addItems(["사무·관리직", "생산·현장직", "전문·연구직", "서비스 및 기타"])
#     layout.addWidget(job)
# 
#     layout.addWidget(QLabel("알림 수신 동의:"))
#     yes = QRadioButton("동의")
#     no = QRadioButton("거부")
#     yes.setChecked(True)
#     group = QButtonGroup(dialog)
#     group.addButton(yes)
#     group.addButton(no)
#     layout.addWidget(yes)
#     layout.addWidget(no)
# 
#     buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#     buttons.accepted.connect(dialog.accept)
#     buttons.rejected.connect(dialog.reject)
#     layout.addWidget(buttons)
# 
#     dialog.setLayout(layout)
#     return dialog, nick, job, yes
# 
# app = QApplication(sys.argv)
# dialog, nick, job, yes = create_profile_dialog()
# if dialog.exec() == QDialog.Accepted:
#     print("닉네임:", nick.text())
#     print("직업:", job.currentText())
#     print("알림 수신:", "동의" if yes.isChecked() else "거부")
# else:
#     print("취소됨")

# [코드 조각]
# dialog, nick, job, yes = create_profile_dialog()
# if dialog.exec() == QDialog.Accepted:
#     print("닉네임:", nick.text())
#     print("직업:", job.currentText())
#     print("알림 수신:", "동의" if yes.isChecked() else "거부")
# else:
#     print("취소됨")
