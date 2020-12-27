'''
File name : main.py
Location : src.gui
Author : Imanpal Singh <imanpalsingh@gmail.com>
'''
'''
Change log:

28-12-20 :

    1) Added Window header and border
    2) Window is now dragable

'''

import sys
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtWidgets import QLabel, QMainWindow, QToolBar, QFileDialog
from PyQt5.QtWidgets import QAction, QStatusBar,QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout,QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


from src.gui.home import Home
from src.gui.analyze import Analyze

import qdarkstyle
from src.gui import stylesheet as css

class Main(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
        
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.setStyleSheet(self.styleSheet() + css.cnormal)
        self.setWindowTitle("Coronavirus Detection from X-rays using Neural Networks")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(500, 250, 1000, 500)
        self.offset = None
        self.loadHome()
        
        
        #self.loadAnalyze()

    def loadHome(self):
        self.home = Home()
        self.setCentralWidget(self.home)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)
        


    
app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()