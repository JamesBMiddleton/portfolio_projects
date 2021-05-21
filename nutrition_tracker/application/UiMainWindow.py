from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QLineEdit, QVBoxLayout, QTableWidget, QLabel)

       
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850,1020)
        MainWindow.setMinimumSize(QtCore.QSize(844, 1008))
        MainWindow.setMaximumSize(QtCore.QSize(844, 1008))
        
        font = QtGui.QFont()
        font.setPointSize(11)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(9, 39, 835, 969))
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.vis_pg = QtWidgets.QWidget()
        self.vis_pg.setObjectName("vis_pg")
        self.stackedWidget.addWidget(self.vis_pg)
        
        self.diary_pg = QtWidgets.QWidget()
        self.diary_pg.setObjectName("diary_pg")
        self.stackedWidget.addWidget(self.diary_pg)
        
        self.search_pg = QtWidgets.QWidget()
        self.search_pg.setObjectName("search_pg")
        
        self.search_field = QLineEdit()    
        self.search_field.setFixedWidth(500)
        self.search_field.setAlignment(QtCore.Qt.AlignHCenter)
        self.search_field.setStyleSheet('font-size: 15px; height: 20px')
            
        self.weight_field = QLineEdit()    
        self.weight_field.setFixedWidth(70)
        self.weight_field.setAlignment(QtCore.Qt.AlignHCenter)
        self.weight_field.setStyleSheet('font-size: 15px; height: 20px') 
        
        self.search_text = QLabel()
        self.search_text.setText('Please search for a food:')
        self.search_text.setStyleSheet('font: bold 12px; height: 20px') 
        
        self.weight_text = QLabel()
        self.weight_text.setText('Weight (kg):')
        self.weight_text.setStyleSheet('font: bold 12px; height: 20px')
        
        self.m_btn = QtWidgets.QPushButton(self.search_pg)
        self.m_btn.setGeometry(QtCore.QRect(324, 280, 89, 25))
        self.m_btn.setText('Male')
        
        self.f_btn = QtWidgets.QPushButton(self.search_pg)
        self.f_btn.setGeometry(QtCore.QRect(420, 280, 89, 25))
        self.f_btn.setText('Female')
        
        self.plus_btn = QtWidgets.QPushButton(self.centralwidget)
        self.plus_btn.setGeometry(QtCore.QRect(802, 10, 31, 25))
        self.plus_btn.setFont(font)
        self.plus_btn.setObjectName("plus_btn")
        
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(10, 10, 31, 25))
        self.back_btn.setFont(font)
        self.back_btn.setObjectName("back_btn")
        
        self.search_btn = QtWidgets.QPushButton(self.centralwidget)
        self.search_btn.setGeometry(QtCore.QRect(48, 10, 89, 25))
        self.search_btn.setFont(font)
        self.search_btn.setObjectName("search_btn")
        
        self.diary_btn = QtWidgets.QPushButton(self.centralwidget)
        self.diary_btn.setGeometry(QtCore.QRect(145, 10, 89, 25))
        self.diary_btn.setFont(font)
        self.diary_btn.setObjectName("diary_btn")
        
        self.gram_text = QtWidgets.QLabel(self.centralwidget)
        self.gram_text.setText('Amount (g):')
        self.gram_text.setGeometry(QtCore.QRect(645, 10, 150, 25))
        self.gram_text.setStyleSheet('font-size: 15px; height: 20px') 
        self.gram_text.setObjectName("gram_field")
        
        self.gram_field = QtWidgets.QLineEdit(self.centralwidget)
        self.gram_field.setGeometry(QtCore.QRect(743, 10, 50, 25))
        self.gram_field.setAlignment(QtCore.Qt.AlignHCenter)
        self.gram_field.setStyleSheet('font-size: 15px; height: 20px') 
        self.gram_field.setObjectName("gram_field")
        
        self.make_table()
        
        mainLayout = QVBoxLayout()
        mainLayout.addSpacing(300)
        mainLayout.addWidget(self.weight_text)
        mainLayout.addSpacing(1)
        mainLayout.addWidget(self.weight_field)   
        mainLayout.addSpacing(1)
        mainLayout.addWidget(self.search_text)
        mainLayout.addSpacing(1)
        mainLayout.addWidget(self.search_field)
        mainLayout.addSpacing(600)
        
        self.search_pg.setLayout(mainLayout)
        self.stackedWidget.addWidget(self.search_pg)
        
        mainLayout.setAlignment(self.weight_text, QtCore.Qt.AlignHCenter)
        mainLayout.setAlignment(self.search_text, QtCore.Qt.AlignHCenter)
        mainLayout.setAlignment(self.weight_field, QtCore.Qt.AlignHCenter)
        mainLayout.setAlignment(QtCore.Qt.AlignHCenter)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def make_table(self):
        self.table_pg = QtWidgets.QWidget()
        self.table_pg.setObjectName('table_pg')
        mainLayout = QVBoxLayout()
        self.table = QTableWidget(30, 2)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 749)
        self.table.setColumnWidth(1, 52)
        self.table.setStyleSheet('font-size: 13px')
        mainLayout.addWidget(self.table)
        self.table_pg.setLayout(mainLayout)
        self.stackedWidget.addWidget(self.table_pg)

    def hide_righthand_widgets(self):
        self.plus_btn.hide()
        self.gram_text.hide()
        self.gram_field.hide()
        
    def show_righthand_widgets(self):
        self.plus_btn.show()
        self.gram_text.show()
        self.gram_field.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Nutrition-Tracker"))
        self.back_btn.setText(_translate("MainWindow", "◁"))
        self.plus_btn.setText(_translate("MainWindow", "+"))
        self.search_btn.setText(_translate("MainWindow", "Search"))
        self.diary_btn.setText(_translate("MainWindow", "Diary"))
