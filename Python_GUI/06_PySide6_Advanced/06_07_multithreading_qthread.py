# -*- coding: utf-8 -*-
"""
교재 예제 파일: 멀티스레딩과 QThread
"""

import sys
import time
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QProgressBar, QVBoxLayout
)
from PySide6.QtCore import QThread, Signal

class Worker(QThread):
    progress = Signal(int)

    def __init__(self):
        super().__init__()
        self._running = True       # 작업을 계속할지 나타내는 플래그

    def run(self):
        count = 0
        while self._running and count < 100:
            time.sleep(0.1)
            count += 1
            self.progress.emit(count)

    def stop(self):
        self._running = False      # 플래그를 내려 run()의 반복을 끝낸다


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.bar = QProgressBar()
        self.start_btn = QPushButton("별도의 스레드 시작")
        self.stop_btn = QPushButton("플래그 이용한 중지")
        self.start_btn.clicked.connect(self.start_work)
        self.stop_btn.clicked.connect(self.stop_work)

        layout = QVBoxLayout()
        layout.addWidget(self.bar)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        self.setLayout(layout)

    def start_work(self):
        self.worker = Worker()
        self.worker.progress.connect(self.bar.setValue)
        self.worker.start()

    def stop_work(self):
        if hasattr(self, "worker") and self.worker.isRunning():
            self.worker.stop()     # 플래그를 내려 안전하게 종료 요청

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

# ==================================================
# 참고 예제 코드 (Reference Code)
# ==================================================

# [다른 예제 코드]
# import sys
# import time
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
# )
# 
# def heavy_task():
#     for i in range(10):
#         time.sleep(1)              # 무거운 작업 흉내
#     label.setText("작업 완료!")
# 
# app = QApplication(sys.argv)
# window = QWidget()
# 
# label = QLabel("대기 중")
# button = QPushButton("스레드 분리 전 무거운 작업 시작")
# button.clicked.connect(heavy_task)
# 
# layout = QVBoxLayout()
# layout.addWidget(label)
# layout.addWidget(button)
# window.setLayout(layout)
# 
# window.show()
# sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# import time
# from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QProgressBar
# from PySide6.QtCore import QThread, Signal
# 
# class Worker(QThread):
#     progress = Signal(int)
# 
#     def run(self):
#         for i in range(1, 101):
#             time.sleep(0.05)
#             self.progress.emit(i)    # ① 작업 스레드: 진행률 시그널 발생
# 
# 
# class MainWindow(QWidget): 
#     def __init__(self):
#         super().__init__()
# 
#         self.progress_bar = QProgressBar()
#         self.start_btn = QPushButton("스레드로 분리된 무거운 작업 시작")
#         self.start_btn.clicked.connect(self.start_work)
# 
#         layout = QVBoxLayout(self) 
#         layout.addWidget(self.progress_bar)
#         layout.addWidget(self.start_btn)
# 
#     def start_work(self):
#         self.start_btn.setEnabled(False)
#         self.worker = Worker()
# 
#         # ② 메인 스레드: 시그널을 받아 UI 안전하게 갱신
#         self.worker.progress.connect(self.progress_bar.setValue) 
#         self.worker.finished.connect(lambda: self.start_btn.setEnabled(True)) 
# 
#         self.worker.start()
# 
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

# [다른 예제 코드]
# import sys
# import time
# from PySide6.QtCore import QObject, QThread, Signal
# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar
# 
# 
# class Worker(QObject):             # QThread가 아니라 QObject를 상속
#     progress = Signal(int)
#     finished = Signal()
# 
#     def run(self):
#         for i in range(1, 51):
#             time.sleep(0.05)
#             self.progress.emit(i * 2)
#         self.finished.emit()
# 
# 
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()    
#         self.pbar = QProgressBar(self)
#         self.btn = QPushButton('moveToThread 시작', self)
#         self.btn.clicked.connect(self.start_thread)
# 
#         vbox = QVBoxLayout()
#         vbox.addWidget(self.pbar)
#         vbox.addWidget(self.btn)
#         self.setLayout(vbox)
# 
#         self.show()
# 
#     def start_thread(self):
#         self.btn.setEnabled(False)
#         self.pbar.setValue(0)
# 
#         self.thread = QThread()
#         self.worker = Worker()
# 
#         self.worker.moveToThread(self.thread)        # 작업 객체를 스레드로 이동
# 
#         self.thread.started.connect(self.worker.run) # 스레드가 시작되면 run 실행
#         self.worker.progress.connect(self.pbar.setValue)
# 
#         self.worker.finished.connect(self.thread.quit)
#         self.worker.finished.connect(lambda: self.btn.setEnabled(True))
# 
#         self.thread.start()
# 
# 
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_win = MainWindow()
#     sys.exit(app.exec())

# [코드 조각]
# from PySide6.QtCore import QThread
# 
# class Worker(QThread):
#     def run(self):                 # start()를 부르면 이 메서드가 새 스레드에서 실행
#         for i in range(5):
#             time.sleep(1)

# [코드 조각]
# class Worker(QThread):
#     progress = Signal(int)
# 
#     def __init__(self, total):
#         super().__init__()
#         self.total = total         # 작업에 필요한 값을 저장
# 
#     def run(self):
#         for i in range(1, self.total + 1):
#             time.sleep(0.5)
#             self.progress.emit(int(i / self.total * 100))
