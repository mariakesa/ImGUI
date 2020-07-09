import sys

from PyQt5.QtCore import QSize,Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore

from pathlib import Path

from moviepy.editor import VideoFileClip

from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cwidget = QtGui.QWidget(self)
        self.setCentralWidget(self.cwidget)
        self.l0 = QtGui.QGridLayout()
        #layout = QtGui.QFormLayout()
        self.cwidget.setLayout(self.l0)

        self.make_seconds_input()

        self.make_file_loader()

        self.make_file_saver()

        self.make_text_box()



    def make_seconds_input(self):
        self.begin_interval = QtGui.QLabel("Beginning:")
        self.begin_interval.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #self.begin_interval.setStyleSheet("color: white;")
        self.begin_interval.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
        self.l0.addWidget(self.begin_interval,  4, 1, 1, 3)

        self.seconds_begin=QtGui.QLineEdit()
        self.seconds_begin.setText("0")
        self.seconds_begin.setFixedWidth(35)
        self.l0.addWidget(self.seconds_begin, 4, 5, 1, 2)

        self.end_interval = QtGui.QLabel("End:")
        self.end_interval.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #self.end_interval.setStyleSheet("color: white;")
        self.end_interval.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
        self.l0.addWidget(self.end_interval,  4, 7, 1, 2)

        self.seconds_end=QtGui.QLineEdit()
        self.seconds_end.setText("10")
        self.seconds_end.setFixedWidth(35)
        self.l0.addWidget(self.seconds_end, 4, 10, 1, 2)

        self.fps_txt = QtGui.QLabel("Frames per second:")
        self.fps_txt.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #self.end_interval.setStyleSheet("color: white;")
        self.fps_txt.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
        self.l0.addWidget(self.fps_txt,  4, 14, 1, 2)

        self.fps=QtGui.QLineEdit()
        self.fps.setText("10")
        self.fps.setFixedWidth(35)
        self.l0.addWidget(self.fps, 4, 17, 1, 2)

        self.add_btn = QtGui.QPushButton("Add interval", self)
        #self.add_btn.clicked.connect(lambda: self.open_file())
        self.l0.addWidget(self.add_btn, 4, 20, 1, 2)


    def make_file_loader(self):
        self.btn = QtGui.QPushButton("Select File...", self)
        self.btn.clicked.connect(lambda: self.open_file())
        self.l0.addWidget(self.btn, 1, 1, 1, 2)

    def make_file_saver(self):
        self.btn_save = QtGui.QPushButton("Save File...", self)
        #self.btn.clicked.connect(lambda: self.open_file())
        self.l0.addWidget(self.btn_save, 1, 4, 1, 2)


    def open_file(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)

        if fname[0]:
            #f = open(fname[0], 'r')
            self.clip = VideoFileClip(fname[0])

    def make_text_box(self):
        self.selected = QtWidgets.QTextBrowser()
        self.selected.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.l0.addWidget(self.selected, 6, 1, 10, 20)

app=QApplication(sys.argv)

window=MainWindow()
window.show()

app.exec_()
