'''
File name : home.py
Location : src.gui
Author : Imanpal Singh <imanpalsingh@gmail.com>
'''
'''
Change log:

28-12-20 :

    1) Added Window header and border
    2) Window is now dragable

'''

from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtWidgets import QLabel, QMainWindow, QToolBar, QFileDialog
from PyQt5.QtWidgets import QAction, QStatusBar,QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout,QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.gui.analyze import Analyze
import os
from src.gui import stylesheet as css


class Home(QWidget):

    def __init__(self, *args, **kwargs):

        super(Home,self).__init__(*args, **kwargs)
        self.folder = ''
        self.success = False
        
        self.setStyleSheet('background-color : transparent; ')
        self.load_GUI()

    def load_GUI(self):

        self.header()
        self.directory_selector()
        self.conformation()
        self.credits()
        self.window_header()
        


    def window_header(self):
        self.heading = QLabel(self)
        self.heading.setText(" Coronavirus Detection from X-rays using Neural Networks")
        self.heading.setMinimumHeight(45)
        self.heading.move(0,0)
        self.heading.setMinimumWidth(1000)
        self.heading.setStyleSheet(css.windowHeader)

    def header(self):

        self.heading = QLabel(self)
        self.heading.setText("Data Extraction")
        self.heading.setMinimumHeight(50)
        self.heading.move(400,100)
        self.heading.setMinimumWidth(180)

        self.heading.setStyleSheet(css.head)
    
    def directory_selector(self):

        self.directory_text  = QLineEdit('', self)
        self.directory_text.move(280,225)
        self.directory_text.setFixedSize(350,40)
        self.directory_text.setStyleSheet(css.dirText + 'border-color:white;')
        self.directory_text.setPlaceholderText("Enter Directory containing X-ray Images")

        self.directory_select = QPushButton('Browse', self, objectName='upload')
        self.directory_select.setFixedSize(5,40)
        self.directory_select.move(630,225)
        self.directory_select.setStyleSheet(css.dirButton)
        self.directory_select.setCursor(Qt.PointingHandCursor)
        self.directory_select.clicked.connect(self.open_directory_select)
    
    def conformation(self):
        self.analyze = QPushButton('Analyze', self, objectName='upload')
        self.analyze.setFixedSize(5,40)
        self.analyze.move(400,290)
        self.analyze.setStyleSheet(css.conform)
        self.analyze.setCursor(Qt.PointingHandCursor)
        self.analyze.clicked.connect(self.analyze_direcotry)
        
        self.exit = QPushButton('Exit', self, objectName='exit')
        self.exit.setFixedSize(5,40)
        self.exit.move(500,290)
        self.exit.setStyleSheet(css.cexit)
        self.exit.clicked.connect(qApp.quit)
        self.exit.setCursor(Qt.PointingHandCursor)
    

    def credits(self):

        self.made_by = QLabel(self)
        self.made_by.setText("   Made by\nImanpal Singh")
        self.made_by.setMinimumHeight(100)
        self.made_by.move(450,390)
        self.made_by.setMinimumWidth(200)
        self.made_by.setStyleSheet('font-size : 13px; color:white;')
    

    ### SLOTS ###

    def analyze_direcotry(self):

        if self.directory_text.text() =='':

            self.directory_text.setStyleSheet(css.dirText + 'border-color:red;')
            self.directory_select.setStyleSheet(css.dirButton + 'border-color:red')
            
        else:
            self.directory_text.setStyleSheet(css.dirText + 'border-color:white;')
            self.directory_select.setStyleSheet(css.dirButton + 'border-color:white')
            self.success = True
            self._analyze()
            

    def open_directory_select(self):
        self.directory_text.clear()
        self.folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.directory_text.insert(self.folder)
        self.directory_text.setStyleSheet(css.dirText + 'border-color:white;')
        self.directory_select.setStyleSheet(css.dirButton + 'border-color:white')



    def _analyze(self):

        try:

            self.files_num = len(os.listdir(self.directory_text.text()))
            
        except:

            self.directory_text.clear()
            self.directory_text.insert("Directory Doesn't exist")
            self.directory_text.setStyleSheet(css.dirText + 'border-color:red;')
            self.directory_select.setStyleSheet(css.dirButton + 'border-color:red')
            print(self.directory_text.text())
            return

        self.path = self.directory_text.text()
        self.directory_text.clear()
        self.analyzeOn = Analyze(self.path)
        self.analyzeOn.show()
        


