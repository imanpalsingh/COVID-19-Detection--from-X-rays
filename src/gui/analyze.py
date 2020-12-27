'''
File name : analyze.py
Location : src.gui
Author : Imanpal Singh <imanpalsingh@gmail.com>
'''
'''
Change log:

28-12-20 :

    1) Added download as Excel file feature

'''

from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication, QPushButton, QSizePolicy
from PyQt5.QtWidgets import QLabel, QMainWindow, QToolBar, QFileDialog, QHeaderView
from PyQt5.QtWidgets import QAction, QStatusBar,QCheckBox, QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout,QLineEdit,QAbstractScrollArea,QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QColor
import qdarkstyle
import os
from src.data.generators import create_new
import pandas as pd
from src.gui import stylesheet as css

class Analyze(QWidget):

   def __init__(self,dir, *args, **kwargs):

      super(Analyze,self).__init__(*args, **kwargs)

      
      self.setStyleSheet(qdarkstyle.load_stylesheet())
      self.setStyleSheet(self.styleSheet() + css.cWidget)
      self.setWindowFlags(Qt.FramelessWindowHint)
      self.setGeometry(500, 250, 997, 497)
      
      self.dir = dir
      self.files_num = len(os.listdir(self.dir))

      self.offset = None
      self.load_GUI()
      self.setWindowTitle("Analyzing X-rays")
      
      

   def load_GUI(self):

      self.header()
      self.wait_until_load()
      self.close_analyze()
      self.window_header()
      self.to_excel()
      self.show_result()

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
        

   def window_header(self):
      self.heading = QLabel(self)
      self.heading.setText(" Coronavirus Detection from X-rays using Neural Networks")
      self.heading.setMinimumHeight(45)
      self.heading.move(0,0)
      self.heading.setMinimumWidth(1000)
      self.heading.setStyleSheet(css.windowHeader)

   def wait_until_load(self):

   
      self._continue()

   def _continue(self):

      self.files, self.data = create_new(self.dir)

   def show_result(self):

      self.result_table = QTableWidget(self)
      self.result_table.setRowCount(len(self.files )+ 1)
      self.result_table.setColumnCount(3)

      self.result_table.setItem(0,0, QTableWidgetItem(" Identification"))
      self.result_table.setItem(0,1, QTableWidgetItem(" Diagnosis"))
      self.result_table.setItem(0,2, QTableWidgetItem(" Confidence"))
      

      #Filling data

      for row in range(0,len(self.files)):

            detected = "Internal Error"
            self.result_table.setItem(row+1,0, QTableWidgetItem(" " + str(self.files[row])))
            pred = max(self.data[row])

            if pred < 0.5:
               detected = "Negative"
               
            else:
               detected = "Positive"
               
            
            self.result_table.setItem(row+1,1,QTableWidgetItem(" " + detected))
            self.result_table.setItem(row+1,2,QTableWidgetItem(" " + str(max(self.data[row]))))
            
            

      self.result_table.move(50,150)
      self.result_table.verticalHeader().setVisible(False)
      self.result_table.horizontalHeader().setVisible(False)



      self.result_table.setShowGrid(True)
      #self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
      self.result_table.setFocusPolicy(Qt.NoFocus)
      self.result_table.setStyleSheet('''
      QTableWidget::item{background-color:#202122; }''')

   
      self.result_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
      self.result_table.setMinimumSize(900,750)
      
      font = QFont()
      font.setBold(True)
      font.setPixelSize(18)
      self.result_table.item(0,0).setFont(font)
      self.result_table.item(0,1).setFont(font)
      self.result_table.item(0,2).setFont(font)
      

      self.colhead = self.result_table.horizontalHeader()       
      self.colhead.setSectionResizeMode(0, QHeaderView.Stretch)
      self.colhead.setSectionResizeMode(1, QHeaderView.Stretch)
      self.colhead.setSectionResizeMode(2, QHeaderView.Stretch)

   


   def header(self):

        self.heading = QLabel(self)
        self.heading.setText("Analysis")
        self.heading.setMinimumHeight(50)
        self.heading.move(450,55)
        self.heading.setMinimumWidth(100)
        self.heading.setStyleSheet(css.head)
   
   def close_analyze(self):
      self.exit = QPushButton('Close', self)
      self.exit.setFixedSize(5,40)
      self.exit.move(500,400)
      self.exit.setStyleSheet(css.conform)
      self.exit.clicked.connect(self.close)
      self.exit.setCursor(Qt.PointingHandCursor)


   def to_excel(self):

      self.excel = QPushButton('Download', self)
      self.excel.setFixedSize(5,40)
      self.excel.move(400,400)
      self.excel.setStyleSheet(css.conform)
      self.excel.setCursor(Qt.PointingHandCursor)
      self.excel.clicked.connect(self.open_directory_save)

   def open_directory_save(self):
      folder = QFileDialog.getSaveFileName(self, "Select destination folder and file name", "", "Excel Files (*.xlsx)")[0]
      
      if folder == '' : return
      
      columns = ['Identification', 'Result', 'Confidence (Relative to Positive)']

      df = []
      for row in range(0,len(self.files)):

            dfrow = []
            pred = max(self.data[row])

            if pred < 0.5:
               detected = "Negative"
            else:
               detected = "Positive"
            
            dfrow.append(self.files[row])
            dfrow.append(detected)
            dfrow.append(max(self.data[row]))
         
            df.append(dfrow)
      
      out_file = pd.DataFrame(df,columns=columns)
      out_file.to_excel(folder + '.xlsx')
   
   

   
    

     
    