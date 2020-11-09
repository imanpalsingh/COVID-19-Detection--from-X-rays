from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication, QPushButton, QSizePolicy
from PyQt5.QtWidgets import QLabel, QMainWindow, QToolBar, QFileDialog, QHeaderView
from PyQt5.QtWidgets import QAction, QStatusBar,QCheckBox, QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout,QLineEdit,QAbstractScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import qdarkstyle
import os
import numpy as np
from src.data.generators import create_new

class Analyze(QWidget):

   def __init__(self,dir, *args, **kwargs):

      super(Analyze,self).__init__(*args, **kwargs)

      self.cssHead = '''font-size : 35px;
         border: 1px solid white;
         border-top:hidden;
         border-left:hidden;
         border-right:hidden;
         border-radius:0px;
         '''
      self.cssConform = '''
        background-color:transparent;
        border : none;
        font-size : 14px;
        border : 1px solid white;  
         '''
      self.dir = dir
      self.setWindowTitle("Analyzing X-rays")
      self.cnormal = 'QWidget {border: 1px solid white; border-radius : 4px; background-color : #202122;}'
      self.setStyleSheet(qdarkstyle.load_stylesheet())
      self.setStyleSheet(self.styleSheet() + self.cnormal)
      self.setWindowFlags(Qt.FramelessWindowHint)
      self.setGeometry(500, 250, 1000, 500)

      self.files_num = len(os.listdir(self.dir))
      self.cssloading= '''font-size : 18px;
         border: none;
         '''
      self.load_GUI()


   def load_GUI(self):

      self.header()
      self.wait_until_load()
      self.show_result()
      self.close_analyze()


   def wait_until_load(self):

   
      self._continue()

   def _continue(self):

      self.files, self.data = create_new(self.dir)

   def show_result(self):

      self.result_table = QTableWidget(self)
      self.result_table.setRowCount(len(self.files )+ 1)
      self.result_table.setColumnCount(3)

      self.result_table.setItem(0,0, QTableWidgetItem("Identification"))
      self.result_table.setItem(0,1, QTableWidgetItem("Diagnosis"))
      self.result_table.setItem(0,2, QTableWidgetItem("Confidence"))

      #Filling data
      print(self.files)
      for row in range(0,len(self.files)):

            detected = "Internal Error"
            self.result_table.setItem(row+1,0, QTableWidgetItem(str(self.files[row])))
            pred = np.argmax(self.data[row])
            if pred == 1:
               detected = "Negative"
            elif pred == 0:
               detected = "Positive"
            
            self.result_table.setItem(row+1,1,QTableWidgetItem(detected))
            self.result_table.setItem(row+1,2,QTableWidgetItem(str(np.max(self.data[row]*100.0))))

      self.result_table.move(50,150)
      self.result_table.verticalHeader().setVisible(False)
      self.result_table.horizontalHeader().setVisible(False)

      self.result_table.setShowGrid(False)
      #self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
      self.result_table.setFocusPolicy(Qt.NoFocus)
      self.result_table.setStyleSheet('''
      QTableWidget::item{background-color:#202122; }
      QTableWidget::item:hover{color:white; }
   
      ''')

   
      self.result_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
      self.result_table.setMinimumSize(900,750)

      self.colhead = self.result_table.horizontalHeader()       
      self.colhead.setSectionResizeMode(0, QHeaderView.Stretch)
      self.colhead.setSectionResizeMode(1, QHeaderView.Stretch)
      self.colhead.setSectionResizeMode(2, QHeaderView.Stretch)


   def header(self):

        self.heading = QLabel(self)
        self.heading.setText("Covid-19 Detection from X-rays")
        self.heading.setMinimumHeight(100)
        self.heading.move(220,40)
        self.heading.setMinimumWidth(500)
        self.heading.setFont(QFont('MonoSpace'))
        self.heading.setStyleSheet(self.cssHead)
   
   def close_analyze(self):
      self.exit = QPushButton('Close', self)
      self.exit.setFixedSize(5,40)
      self.exit.move(450,400)
      self.exit.setStyleSheet(self.cssConform)
      self.exit.clicked.connect(self.close)
      self.exit.setCursor(Qt.PointingHandCursor)

   
    

     
    