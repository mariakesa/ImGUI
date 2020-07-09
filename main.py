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

from moviepy.editor import *

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

        self.intervals=[]
        self.speed_lst=[]



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

        self.speed_txt = QtGui.QLabel("Speed x:")
        self.speed_txt.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #self.end_interval.setStyleSheet("color: white;")
        self.speed_txt.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
        self.l0.addWidget(self.speed_txt,  4, 14, 1, 2)

        self.speed=QtGui.QLineEdit()
        self.speed.setText("10")
        self.speed.setFixedWidth(35)
        self.l0.addWidget(self.speed, 4, 17, 1, 2)

        self.add_btn = QtGui.QPushButton("Add interval", self)
        self.add_btn.clicked.connect(lambda: self.add_interval())
        self.l0.addWidget(self.add_btn, 4, 20, 1, 2)


    def make_file_loader(self):
        self.btn = QtGui.QPushButton("Select File...", self)
        self.btn.clicked.connect(lambda: self.open_file())
        self.l0.addWidget(self.btn, 1, 1, 1, 2)

    def make_file_saver(self):
        self.btn_save = QtGui.QPushButton("Save File...", self)
        self.btn_save.clicked.connect(lambda: self.save_file())
        self.l0.addWidget(self.btn_save, 1, 4, 1, 2)


    def open_file(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)

        if fname[0]:
            #f = open(fname[0], 'r')
            self.clip = VideoFileClip(fname[0])

        print('FPS ',self.clip.fps)

    def make_text_box(self):
        self.selected = QtWidgets.QTextBrowser()
        self.selected.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.l0.addWidget(self.selected, 6, 1, 10, 20)

    def set_text(self):
        txt=''
        for interval in range(len(self.intervals)):
            txt+='\n'+'Interval: '+self.intervals[interval][0]+', '+self.intervals[interval][1]+', Speed '+self.speed_lst[interval]
        self.selected.setText(txt)

    def add_interval(self):
        beg=self.seconds_begin.text()
        end=self.seconds_end.text()
        speed=self.speed.text()
        self.intervals.append([beg,end])
        self.speed_lst.append(speed)
        print(self.intervals)
        self.set_text()

    def save_file(self):
        print('boom')
        movie_length=self.clip.duration
        self.intervals.sort(key=lambda x: int(x[0]))
        bookmark=0
        result=[]
        clips=[]
        i=0
        for clip in self.intervals:
            if bookmark<int(clip[0]):
                result.append([bookmark, int(clip[0])])
                clips.append(self.clip.subclip(bookmark, int(clip[0])))
                print('bkm',bookmark)
            result.append([int(clip[0]),int(clip[1])])
            bookmark=int(clip[1])
            mod_clp=self.clip.subclip(int(clip[0]),int(clip[1]))
            mod_clp=mod_clp.speedx(factor=int(self.speed_lst[i]))
            clips.append(mod_clp)
            i+=1
        print(result)
        print(clips)
        if bookmark<movie_length:
            result.append([bookmark,movie_length])
            clips.append(self.clip.subclip(bookmark,movie_length))
        #self.total_clp=[]
        #for interval in range(len(self.intervals)):
            #new_clip = self.clip.subclip(self.intervals[interval][0],self.interval[1])
        final = concatenate_videoclips(clips)
        final.write_videofile("new_clip.mov", codec = "libx264")


app=QApplication(sys.argv)

window=MainWindow()
window.show()

app.exec_()
