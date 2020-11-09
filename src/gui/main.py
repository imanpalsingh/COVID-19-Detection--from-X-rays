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

class Main(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
        
        self.cnormal = 'QMainWindow {border: 1px solid gray; border-radius : 4px; background-color : #202122;}'
        
        self.setWindowTitle("Covid-19 Detection from X-rays")
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.setStyleSheet(self.styleSheet() + self.cnormal)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(500, 250, 1000, 500)

        self.loadHome()
        #self.loadAnalyze()

    def loadHome(self):
        self.home = Home()
        self.setCentralWidget(self.home)
        
    def loadAnalyze(self):
        self.analyze = Analyze()
        self.analyze.show()


    
app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()