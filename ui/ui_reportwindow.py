# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ReportWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QDateTimeEdit,
    QDoubleSpinBox, QGridLayout, QGroupBox, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpinBox, QTabWidget,
    QTableView, QTableWidget, QTableWidgetItem, QTextEdit,
    QWidget)

class Ui_reportWindow(object):
    def setupUi(self, reportWindow):
        if not reportWindow.objectName():
            reportWindow.setObjectName(u"reportWindow")
        reportWindow.resize(1913, 996)
        self.action = QAction(reportWindow)
        self.action.setObjectName(u"action")
        self.action_2 = QAction(reportWindow)
        self.action_2.setObjectName(u"action_2")
        self.action_3 = QAction(reportWindow)
        self.action_3.setObjectName(u"action_3")
        self.action_4 = QAction(reportWindow)
        self.action_4.setObjectName(u"action_4")
        self.action_5 = QAction(reportWindow)
        self.action_5.setObjectName(u"action_5")
        self.action_6 = QAction(reportWindow)
        self.action_6.setObjectName(u"action_6")
        self.action_7 = QAction(reportWindow)
        self.action_7.setObjectName(u"action_7")
        self.action_8 = QAction(reportWindow)
        self.action_8.setObjectName(u"action_8")
        self.action_9 = QAction(reportWindow)
        self.action_9.setObjectName(u"action_9")
        self.action_10 = QAction(reportWindow)
        self.action_10.setObjectName(u"action_10")
        self.action_11 = QAction(reportWindow)
        self.action_11.setObjectName(u"action_11")
        self.action_12 = QAction(reportWindow)
        self.action_12.setObjectName(u"action_12")
        self.action_13 = QAction(reportWindow)
        self.action_13.setObjectName(u"action_13")
        self.action_14 = QAction(reportWindow)
        self.action_14.setObjectName(u"action_14")
        self.action_15 = QAction(reportWindow)
        self.action_15.setObjectName(u"action_15")
        self.centralwidget = QWidget(reportWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QRect(0, 30, 1960, 951))
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.groupBox_9 = QGroupBox(self.tab_5)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setGeometry(QRect(10, 0, 331, 71))
        self.gridLayoutWidget_25 = QWidget(self.groupBox_9)
        self.gridLayoutWidget_25.setObjectName(u"gridLayoutWidget_25")
        self.gridLayoutWidget_25.setGeometry(QRect(10, 20, 71, 41))
        self.gridLayout_25 = QGridLayout(self.gridLayoutWidget_25)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(0, 0, 0, 0)
        self.label_49 = QLabel(self.gridLayoutWidget_25)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_25.addWidget(self.label_49, 0, 0, 1, 1)

        self.gridLayoutWidget_26 = QWidget(self.groupBox_9)
        self.gridLayoutWidget_26.setObjectName(u"gridLayoutWidget_26")
        self.gridLayoutWidget_26.setGeometry(QRect(80, 20, 241, 41))
        self.gridLayout_26 = QGridLayout(self.gridLayoutWidget_26)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setContentsMargins(0, 0, 0, 0)
        self.comboBox_13 = QComboBox(self.gridLayoutWidget_26)
        self.comboBox_13.setObjectName(u"comboBox_13")

        self.gridLayout_26.addWidget(self.comboBox_13, 1, 0, 1, 1)

        self.groupBox_12 = QGroupBox(self.tab_5)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setGeometry(QRect(10, 320, 331, 61))
        self.gridLayoutWidget_27 = QWidget(self.groupBox_12)
        self.gridLayoutWidget_27.setObjectName(u"gridLayoutWidget_27")
        self.gridLayoutWidget_27.setGeometry(QRect(10, 20, 311, 28))
        self.gridLayout_27 = QGridLayout(self.gridLayoutWidget_27)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridLayout_27.setContentsMargins(0, 0, 0, 0)
        self.label_56 = QLabel(self.gridLayoutWidget_27)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setMaximumSize(QSize(51, 22))
        self.label_56.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_56.setAutoFillBackground(False)

        self.gridLayout_27.addWidget(self.label_56, 0, 0, 1, 1)

        self.comboBox_14 = QComboBox(self.gridLayoutWidget_27)
        self.comboBox_14.setObjectName(u"comboBox_14")

        self.gridLayout_27.addWidget(self.comboBox_14, 0, 1, 1, 1)

        self.groupBox_13 = QGroupBox(self.tab_5)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setGeometry(QRect(10, 80, 331, 221))
        self.gridLayoutWidget_30 = QWidget(self.groupBox_13)
        self.gridLayoutWidget_30.setObjectName(u"gridLayoutWidget_30")
        self.gridLayoutWidget_30.setGeometry(QRect(10, 20, 311, 41))
        self.gridLayout_30 = QGridLayout(self.gridLayoutWidget_30)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setContentsMargins(0, 0, 0, 0)
        self.label_59 = QLabel(self.gridLayoutWidget_30)
        self.label_59.setObjectName(u"label_59")

        self.gridLayout_30.addWidget(self.label_59, 0, 0, 1, 1)

        self.lineEdit_23 = QLineEdit(self.gridLayoutWidget_30)
        self.lineEdit_23.setObjectName(u"lineEdit_23")

        self.gridLayout_30.addWidget(self.lineEdit_23, 0, 1, 1, 1)

        self.gridLayoutWidget_31 = QWidget(self.groupBox_13)
        self.gridLayoutWidget_31.setObjectName(u"gridLayoutWidget_31")
        self.gridLayoutWidget_31.setGeometry(QRect(10, 70, 311, 95))
        self.gridLayout_31 = QGridLayout(self.gridLayoutWidget_31)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.gridLayout_31.setContentsMargins(0, 0, 0, 0)
        self.textEdit_5 = QTextEdit(self.gridLayoutWidget_31)
        self.textEdit_5.setObjectName(u"textEdit_5")

        self.gridLayout_31.addWidget(self.textEdit_5, 1, 0, 1, 1)

        self.label_60 = QLabel(self.gridLayoutWidget_31)
        self.label_60.setObjectName(u"label_60")

        self.gridLayout_31.addWidget(self.label_60, 0, 0, 1, 1)

        self.gridLayoutWidget_32 = QWidget(self.groupBox_13)
        self.gridLayoutWidget_32.setObjectName(u"gridLayoutWidget_32")
        self.gridLayoutWidget_32.setGeometry(QRect(10, 170, 311, 41))
        self.gridLayout_32 = QGridLayout(self.gridLayoutWidget_32)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.gridLayout_32.setContentsMargins(0, 0, 0, 0)
        self.label_61 = QLabel(self.gridLayoutWidget_32)
        self.label_61.setObjectName(u"label_61")

        self.gridLayout_32.addWidget(self.label_61, 0, 0, 1, 1)

        self.lineEdit_24 = QLineEdit(self.gridLayoutWidget_32)
        self.lineEdit_24.setObjectName(u"lineEdit_24")

        self.gridLayout_32.addWidget(self.lineEdit_24, 0, 1, 1, 1)

        self.groupBox_14 = QGroupBox(self.tab_5)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setGeometry(QRect(350, 0, 1551, 921))
        self.tableView_2 = QTableView(self.groupBox_14)
        self.tableView_2.setObjectName(u"tableView_2")
        self.tableView_2.setGeometry(QRect(10, 20, 791, 851))
        self.pushButton_15 = QPushButton(self.groupBox_14)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setGeometry(QRect(10, 880, 551, 26))
        self.pushButton_6 = QPushButton(self.groupBox_14)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(560, 880, 121, 26))
        self.pushButton_8 = QPushButton(self.groupBox_14)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(680, 880, 121, 26))
        self.groupBox = QGroupBox(self.groupBox_14)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(810, 20, 731, 891))
        self.gridLayoutWidget_33 = QWidget(self.tab_5)
        self.gridLayoutWidget_33.setObjectName(u"gridLayoutWidget_33")
        self.gridLayoutWidget_33.setGeometry(QRect(10, 490, 331, 124))
        self.gridLayout_33 = QGridLayout(self.gridLayoutWidget_33)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.gridLayout_33.setContentsMargins(0, 0, 0, 0)
        self.comboBox_18 = QComboBox(self.gridLayoutWidget_33)
        self.comboBox_18.setObjectName(u"comboBox_18")

        self.gridLayout_33.addWidget(self.comboBox_18, 1, 1, 1, 1)

        self.textEdit_2 = QTextEdit(self.gridLayoutWidget_33)
        self.textEdit_2.setObjectName(u"textEdit_2")

        self.gridLayout_33.addWidget(self.textEdit_2, 2, 0, 1, 2)

        self.comboBox_17 = QComboBox(self.gridLayoutWidget_33)
        self.comboBox_17.setObjectName(u"comboBox_17")

        self.gridLayout_33.addWidget(self.comboBox_17, 0, 1, 1, 1)

        self.label_66 = QLabel(self.gridLayoutWidget_33)
        self.label_66.setObjectName(u"label_66")

        self.gridLayout_33.addWidget(self.label_66, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.label_68 = QLabel(self.gridLayoutWidget_33)
        self.label_68.setObjectName(u"label_68")

        self.gridLayout_33.addWidget(self.label_68, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.label_64 = QLabel(self.tab_5)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setGeometry(QRect(10, 460, 101, 21))
        self.label_62 = QLabel(self.tab_5)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setGeometry(QRect(10, 400, 81, 21))
        self.label_63 = QLabel(self.tab_5)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setGeometry(QRect(10, 430, 101, 21))
        self.spinBox_6 = QSpinBox(self.tab_5)
        self.spinBox_6.setObjectName(u"spinBox_6")
        self.spinBox_6.setGeometry(QRect(120, 400, 61, 21))
        self.comboBox_16 = QComboBox(self.tab_5)
        self.comboBox_16.setObjectName(u"comboBox_16")
        self.comboBox_16.setGeometry(QRect(120, 430, 211, 21))
        self.tabWidget.addTab(self.tab_5, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.groupBox_6 = QGroupBox(self.tab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(10, 10, 1881, 911))
        self.tableView = QTableView(self.groupBox_6)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(330, 20, 1541, 881))
        self.gridLayoutWidget_24 = QWidget(self.groupBox_6)
        self.gridLayoutWidget_24.setObjectName(u"gridLayoutWidget_24")
        self.gridLayoutWidget_24.setGeometry(QRect(10, 130, 311, 124))
        self.gridLayout_24 = QGridLayout(self.gridLayoutWidget_24)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(0, 0, 0, 0)
        self.label_50 = QLabel(self.gridLayoutWidget_24)
        self.label_50.setObjectName(u"label_50")

        self.gridLayout_24.addWidget(self.label_50, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.comboBox_12 = QComboBox(self.gridLayoutWidget_24)
        self.comboBox_12.setObjectName(u"comboBox_12")

        self.gridLayout_24.addWidget(self.comboBox_12, 0, 1, 1, 1)

        self.label_54 = QLabel(self.gridLayoutWidget_24)
        self.label_54.setObjectName(u"label_54")

        self.gridLayout_24.addWidget(self.label_54, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.comboBox_11 = QComboBox(self.gridLayoutWidget_24)
        self.comboBox_11.setObjectName(u"comboBox_11")

        self.gridLayout_24.addWidget(self.comboBox_11, 1, 1, 1, 1)

        self.textEdit_3 = QTextEdit(self.gridLayoutWidget_24)
        self.textEdit_3.setObjectName(u"textEdit_3")

        self.gridLayout_24.addWidget(self.textEdit_3, 2, 0, 1, 2)

        self.gridLayoutWidget = QWidget(self.groupBox_6)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 30, 311, 92))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(self.gridLayoutWidget)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout.addWidget(self.label_20, 2, 0, 1, 1)

        self.label_19 = QLabel(self.gridLayoutWidget)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout.addWidget(self.label_19, 1, 0, 1, 1)

        self.label_70 = QLabel(self.gridLayoutWidget)
        self.label_70.setObjectName(u"label_70")

        self.gridLayout.addWidget(self.label_70, 0, 0, 1, 1)

        self.comboBox_19 = QComboBox(self.gridLayoutWidget)
        self.comboBox_19.setObjectName(u"comboBox_19")

        self.gridLayout.addWidget(self.comboBox_19, 0, 1, 1, 1)

        self.spinBox_3 = QSpinBox(self.gridLayoutWidget)
        self.spinBox_3.setObjectName(u"spinBox_3")

        self.gridLayout.addWidget(self.spinBox_3, 1, 1, 1, 1)

        self.comboBox_7 = QComboBox(self.gridLayoutWidget)
        self.comboBox_7.setObjectName(u"comboBox_7")

        self.gridLayout.addWidget(self.comboBox_7, 2, 1, 1, 1)

        self.pushButton_14 = QPushButton(self.groupBox_6)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setGeometry(QRect(10, 230, 311, 26))
        self.pushButton_11 = QPushButton(self.groupBox_6)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(10, 260, 311, 26))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.groupBox_7 = QGroupBox(self.tab_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(10, 40, 451, 221))
        self.gridLayoutWidget_13 = QWidget(self.groupBox_7)
        self.gridLayoutWidget_13.setObjectName(u"gridLayoutWidget_13")
        self.gridLayoutWidget_13.setGeometry(QRect(10, 20, 431, 41))
        self.gridLayout_14 = QGridLayout(self.gridLayoutWidget_13)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.label_13 = QLabel(self.gridLayoutWidget_13)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_14.addWidget(self.label_13, 0, 0, 1, 1)

        self.lineEdit_5 = QLineEdit(self.gridLayoutWidget_13)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.gridLayout_14.addWidget(self.lineEdit_5, 0, 1, 1, 1)

        self.gridLayoutWidget_14 = QWidget(self.groupBox_7)
        self.gridLayoutWidget_14.setObjectName(u"gridLayoutWidget_14")
        self.gridLayoutWidget_14.setGeometry(QRect(10, 70, 431, 95))
        self.gridLayout_15 = QGridLayout(self.gridLayoutWidget_14)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.textEdit_4 = QTextEdit(self.gridLayoutWidget_14)
        self.textEdit_4.setObjectName(u"textEdit_4")

        self.gridLayout_15.addWidget(self.textEdit_4, 1, 0, 1, 1)

        self.label_14 = QLabel(self.gridLayoutWidget_14)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_15.addWidget(self.label_14, 0, 0, 1, 1)

        self.gridLayoutWidget_15 = QWidget(self.groupBox_7)
        self.gridLayoutWidget_15.setObjectName(u"gridLayoutWidget_15")
        self.gridLayoutWidget_15.setGeometry(QRect(10, 170, 431, 41))
        self.gridLayout_16 = QGridLayout(self.gridLayoutWidget_15)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_15 = QLabel(self.gridLayoutWidget_15)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_16.addWidget(self.label_15, 0, 0, 1, 1)

        self.lineEdit_6 = QLineEdit(self.gridLayoutWidget_15)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.gridLayout_16.addWidget(self.lineEdit_6, 0, 1, 1, 1)

        self.groupBox_8 = QGroupBox(self.tab_2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(10, 260, 451, 61))
        self.gridLayoutWidget_16 = QWidget(self.groupBox_8)
        self.gridLayoutWidget_16.setObjectName(u"gridLayoutWidget_16")
        self.gridLayoutWidget_16.setGeometry(QRect(10, 20, 431, 28))
        self.gridLayout_17 = QGridLayout(self.gridLayoutWidget_16)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.label_16 = QLabel(self.gridLayoutWidget_16)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMaximumSize(QSize(51, 22))
        self.label_16.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_16.setAutoFillBackground(False)

        self.gridLayout_17.addWidget(self.label_16, 0, 0, 1, 1)

        self.comboBox_5 = QComboBox(self.gridLayoutWidget_16)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.gridLayout_17.addWidget(self.comboBox_5, 0, 1, 1, 1)

        self.groupBox_10 = QGroupBox(self.tab_2)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setGeometry(QRect(10, 320, 451, 561))
        self.gridLayoutWidget_17 = QWidget(self.groupBox_10)
        self.gridLayoutWidget_17.setObjectName(u"gridLayoutWidget_17")
        self.gridLayoutWidget_17.setGeometry(QRect(10, 20, 431, 531))
        self.gridLayout_18 = QGridLayout(self.gridLayoutWidget_17)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.label_26 = QLabel(self.gridLayoutWidget_17)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_18.addWidget(self.label_26, 5, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_25 = QLabel(self.gridLayoutWidget_17)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_18.addWidget(self.label_25, 8, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_24 = QLabel(self.gridLayoutWidget_17)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_18.addWidget(self.label_24, 7, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_17 = QLabel(self.gridLayoutWidget_17)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_18.addWidget(self.label_17, 2, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.comboBox_8 = QComboBox(self.gridLayoutWidget_17)
        self.comboBox_8.setObjectName(u"comboBox_8")

        self.gridLayout_18.addWidget(self.comboBox_8, 8, 1, 1, 1)

        self.lineEdit_2 = QLineEdit(self.gridLayoutWidget_17)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_18.addWidget(self.lineEdit_2, 0, 1, 1, 1)

        self.label_30 = QLabel(self.gridLayoutWidget_17)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_18.addWidget(self.label_30, 0, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.lineEdit_10 = QLineEdit(self.gridLayoutWidget_17)
        self.lineEdit_10.setObjectName(u"lineEdit_10")

        self.gridLayout_18.addWidget(self.lineEdit_10, 5, 1, 1, 1)

        self.lineEdit_8 = QLineEdit(self.gridLayoutWidget_17)
        self.lineEdit_8.setObjectName(u"lineEdit_8")

        self.gridLayout_18.addWidget(self.lineEdit_8, 3, 1, 1, 1)

        self.label_29 = QLabel(self.gridLayoutWidget_17)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_18.addWidget(self.label_29, 3, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.plainTextEdit = QPlainTextEdit(self.gridLayoutWidget_17)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.gridLayout_18.addWidget(self.plainTextEdit, 9, 1, 1, 1)

        self.label_22 = QLabel(self.gridLayoutWidget_17)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_18.addWidget(self.label_22, 4, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.lineEdit_9 = QLineEdit(self.gridLayoutWidget_17)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.gridLayout_18.addWidget(self.lineEdit_9, 4, 1, 1, 1)

        self.lineEdit_13 = QLineEdit(self.gridLayoutWidget_17)
        self.lineEdit_13.setObjectName(u"lineEdit_13")

        self.gridLayout_18.addWidget(self.lineEdit_13, 7, 1, 1, 1)

        self.dateTimeEdit = QDateTimeEdit(self.gridLayoutWidget_17)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")

        self.gridLayout_18.addWidget(self.dateTimeEdit, 1, 1, 1, 1)

        self.lineEdit_12 = QLineEdit(self.gridLayoutWidget_17)
        self.lineEdit_12.setObjectName(u"lineEdit_12")

        self.gridLayout_18.addWidget(self.lineEdit_12, 6, 1, 1, 1)

        self.lineEdit_7 = QLineEdit(self.gridLayoutWidget_17)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.gridLayout_18.addWidget(self.lineEdit_7, 2, 1, 1, 1)

        self.label_23 = QLabel(self.gridLayoutWidget_17)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_18.addWidget(self.label_23, 6, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_33 = QLabel(self.gridLayoutWidget_17)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_18.addWidget(self.label_33, 9, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_31 = QLabel(self.gridLayoutWidget_17)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_18.addWidget(self.label_31, 1, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.groupBox_11 = QGroupBox(self.tab_2)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setGeometry(QRect(470, 40, 341, 841))
        self.label_32 = QLabel(self.groupBox_11)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setGeometry(QRect(10, 60, 121, 20))
        self.lineEdit_14 = QLineEdit(self.groupBox_11)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setGeometry(QRect(130, 60, 201, 21))
        self.gridLayoutWidget_19 = QWidget(self.groupBox_11)
        self.gridLayoutWidget_19.setObjectName(u"gridLayoutWidget_19")
        self.gridLayoutWidget_19.setGeometry(QRect(40, 90, 291, 161))
        self.gridLayout_19 = QGridLayout(self.gridLayoutWidget_19)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.label_28 = QLabel(self.gridLayoutWidget_19)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_19.addWidget(self.label_28, 0, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_27 = QLabel(self.gridLayoutWidget_19)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_19.addWidget(self.label_27, 3, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_36 = QLabel(self.gridLayoutWidget_19)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_19.addWidget(self.label_36, 2, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_37 = QLabel(self.gridLayoutWidget_19)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_19.addWidget(self.label_37, 4, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_35 = QLabel(self.gridLayoutWidget_19)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_19.addWidget(self.label_35, 1, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.comboBox_10 = QComboBox(self.gridLayoutWidget_19)
        self.comboBox_10.setObjectName(u"comboBox_10")

        self.gridLayout_19.addWidget(self.comboBox_10, 1, 1, 1, 1)

        self.lineEdit_15 = QLineEdit(self.gridLayoutWidget_19)
        self.lineEdit_15.setObjectName(u"lineEdit_15")

        self.gridLayout_19.addWidget(self.lineEdit_15, 2, 1, 1, 1)

        self.lineEdit_16 = QLineEdit(self.gridLayoutWidget_19)
        self.lineEdit_16.setObjectName(u"lineEdit_16")

        self.gridLayout_19.addWidget(self.lineEdit_16, 3, 1, 1, 1)

        self.lineEdit_17 = QLineEdit(self.gridLayoutWidget_19)
        self.lineEdit_17.setObjectName(u"lineEdit_17")

        self.gridLayout_19.addWidget(self.lineEdit_17, 4, 1, 1, 1)

        self.comboBox_9 = QComboBox(self.gridLayoutWidget_19)
        self.comboBox_9.setObjectName(u"comboBox_9")

        self.gridLayout_19.addWidget(self.comboBox_9, 0, 1, 1, 1)

        self.gridLayoutWidget_20 = QWidget(self.groupBox_11)
        self.gridLayoutWidget_20.setObjectName(u"gridLayoutWidget_20")
        self.gridLayoutWidget_20.setGeometry(QRect(10, 259, 321, 60))
        self.gridLayout_20 = QGridLayout(self.gridLayoutWidget_20)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.label_40 = QLabel(self.gridLayoutWidget_20)
        self.label_40.setObjectName(u"label_40")

        self.gridLayout_20.addWidget(self.label_40, 0, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_39 = QLabel(self.gridLayoutWidget_20)
        self.label_39.setObjectName(u"label_39")

        self.gridLayout_20.addWidget(self.label_39, 1, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.lineEdit_18 = QLineEdit(self.gridLayoutWidget_20)
        self.lineEdit_18.setObjectName(u"lineEdit_18")

        self.gridLayout_20.addWidget(self.lineEdit_18, 0, 1, 1, 1)

        self.lineEdit_19 = QLineEdit(self.gridLayoutWidget_20)
        self.lineEdit_19.setObjectName(u"lineEdit_19")

        self.gridLayout_20.addWidget(self.lineEdit_19, 1, 1, 1, 1)

        self.gridLayoutWidget_21 = QWidget(self.groupBox_11)
        self.gridLayoutWidget_21.setObjectName(u"gridLayoutWidget_21")
        self.gridLayoutWidget_21.setGeometry(QRect(-70, 320, 401, 92))
        self.gridLayout_21 = QGridLayout(self.gridLayoutWidget_21)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.label_42 = QLabel(self.gridLayoutWidget_21)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_21.addWidget(self.label_42, 1, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_41 = QLabel(self.gridLayoutWidget_21)
        self.label_41.setObjectName(u"label_41")

        self.gridLayout_21.addWidget(self.label_41, 2, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_43 = QLabel(self.gridLayoutWidget_21)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_21.addWidget(self.label_43, 0, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.spinBox_2 = QSpinBox(self.gridLayoutWidget_21)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMinimum(0)
        self.spinBox_2.setMaximum(999999999)

        self.gridLayout_21.addWidget(self.spinBox_2, 0, 1, 1, 1)

        self.doubleSpinBox = QDoubleSpinBox(self.gridLayoutWidget_21)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMaximum(10000000000000000.000000000000000)

        self.gridLayout_21.addWidget(self.doubleSpinBox, 1, 1, 1, 1)

        self.spinBox_4 = QSpinBox(self.gridLayoutWidget_21)
        self.spinBox_4.setObjectName(u"spinBox_4")
        self.spinBox_4.setMaximum(999999999)

        self.gridLayout_21.addWidget(self.spinBox_4, 2, 1, 1, 1)

        self.gridLayoutWidget_22 = QWidget(self.groupBox_11)
        self.gridLayoutWidget_22.setObjectName(u"gridLayoutWidget_22")
        self.gridLayoutWidget_22.setGeometry(QRect(12, 418, 241, 60))
        self.gridLayout_22 = QGridLayout(self.gridLayoutWidget_22)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(0, 0, 0, 0)
        self.label_45 = QLabel(self.gridLayoutWidget_22)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_22.addWidget(self.label_45, 0, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_46 = QLabel(self.gridLayoutWidget_22)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_22.addWidget(self.label_46, 1, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.dateEdit = QDateEdit(self.gridLayoutWidget_22)
        self.dateEdit.setObjectName(u"dateEdit")

        self.gridLayout_22.addWidget(self.dateEdit, 0, 1, 1, 1)

        self.dateEdit_2 = QDateEdit(self.gridLayoutWidget_22)
        self.dateEdit_2.setObjectName(u"dateEdit_2")

        self.gridLayout_22.addWidget(self.dateEdit_2, 1, 1, 1, 1)

        self.gridLayoutWidget_23 = QWidget(self.groupBox_11)
        self.gridLayoutWidget_23.setObjectName(u"gridLayoutWidget_23")
        self.gridLayoutWidget_23.setGeometry(QRect(10, 485, 321, 351))
        self.gridLayout_23 = QGridLayout(self.gridLayoutWidget_23)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_23.setContentsMargins(0, 0, 0, 0)
        self.plainTextEdit_4 = QPlainTextEdit(self.gridLayoutWidget_23)
        self.plainTextEdit_4.setObjectName(u"plainTextEdit_4")

        self.gridLayout_23.addWidget(self.plainTextEdit_4, 1, 1, 1, 1)

        self.label_47 = QLabel(self.gridLayoutWidget_23)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout_23.addWidget(self.label_47, 1, 0, 1, 1)

        self.plainTextEdit_3 = QPlainTextEdit(self.gridLayoutWidget_23)
        self.plainTextEdit_3.setObjectName(u"plainTextEdit_3")

        self.gridLayout_23.addWidget(self.plainTextEdit_3, 0, 1, 1, 1)

        self.label_48 = QLabel(self.gridLayoutWidget_23)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_23.addWidget(self.label_48, 0, 0, 1, 1)

        self.tableWidget = QTableWidget(self.tab_2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(1050, 50, 841, 831))
        self.label_34 = QLabel(self.tab_2)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setGeometry(QRect(10, 10, 271, 31))
        self.label_34.setStyleSheet(u"font: 28pt \"Segoe UI\";")
        self.label_38 = QLabel(self.tab_2)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setGeometry(QRect(1050, 10, 171, 31))
        self.label_38.setStyleSheet(u"font: 28pt \"Segoe UI\";")
        self.pushButton_16 = QPushButton(self.tab_2)
        self.pushButton_16.setObjectName(u"pushButton_16")
        self.pushButton_16.setGeometry(QRect(820, 400, 221, 51))
        self.pushButton_5 = QPushButton(self.tab_2)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(1480, 890, 201, 26))
        self.pushButton_7 = QPushButton(self.tab_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(1690, 890, 201, 26))
        self.textEdit = QTextEdit(self.tab_2)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(1240, 10, 651, 31))
        self.tabWidget.addTab(self.tab_2, "")
        reportWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(reportWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(reportWindow)
    # setupUi

    def retranslateUi(self, reportWindow):
        reportWindow.setWindowTitle(QCoreApplication.translate("reportWindow", u"\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438", None))
        self.action.setText(QCoreApplication.translate("reportWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043e\u0442\u0447\u0435\u0442", None))
        self.action_2.setText(QCoreApplication.translate("reportWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043e\u0442\u0447\u0435\u0442", None))
        self.action_3.setText(QCoreApplication.translate("reportWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043e\u0442\u0447\u0435\u0442", None))
        self.action_4.setText(QCoreApplication.translate("reportWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043a\u0430\u043a...", None))
        self.action_5.setText(QCoreApplication.translate("reportWindow", u"\u041f\u043e\u043b\u043d\u044b\u0439 \u0441\u043f\u0438\u0441\u043e\u043a \u043e\u0442\u0447\u0435\u0442\u043e\u0432", None))
        self.action_6.setText(QCoreApplication.translate("reportWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", None))
        self.action_7.setText(QCoreApplication.translate("reportWindow", u"\u0420\u0430\u0437\u043c\u0435\u0440 \u0448\u0440\u0438\u0444\u0442\u0430", None))
        self.action_8.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0435\u043c\u0430", None))
        self.action_9.setText(QCoreApplication.translate("reportWindow", u"\u0412\u0435\u0440\u0441\u0438\u044f", None))
        self.action_10.setText(QCoreApplication.translate("reportWindow", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0435", None))
        self.action_11.setText(QCoreApplication.translate("reportWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0440\u0430\u0431\u043e\u0447\u0435\u0435 \u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u0435", None))
        self.action_12.setText(QCoreApplication.translate("reportWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u043a\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.action_13.setText(QCoreApplication.translate("reportWindow", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f", None))
        self.action_14.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u0432\u0430\u044f \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u044c", None))
        self.action_15.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u0432\u043e\u0435 \u043f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u0435", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("reportWindow", u"<html><head/><body><p>\u0432</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_9.setTitle(QCoreApplication.translate("reportWindow", u"\u041b\u0438\u0446\u043e, \u0437\u0430\u043f\u043e\u043b\u043d\u044f\u044e\u0449\u0438\u0435\u0435 \u043e\u0442\u0447\u0435\u0442:", None))
        self.label_49.setText(QCoreApplication.translate("reportWindow", u"\u0424\u0418\u041e:", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("reportWindow", u"\u0412\u044b\u0431\u043e\u0440 \u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u044f:", None))
        self.label_56.setText(QCoreApplication.translate("reportWindow", u"\u0424\u0438\u043b\u0438\u0430\u043b:", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("reportWindow", u"\u0420\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435:", None))
        self.label_59.setText(QCoreApplication.translate("reportWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 :", None))
        self.label_60.setText(QCoreApplication.translate("reportWindow", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435:", None))
        self.label_61.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u043f\u0440\u0438\u043a\u0430\u0437\u0430:*", None))
        self.lineEdit_24.setText("")
        self.groupBox_14.setTitle(QCoreApplication.translate("reportWindow", u"\u0420\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0434\u0435\u043d\u0438\u0435", None))
        self.pushButton_15.setText(QCoreApplication.translate("reportWindow", u"\u041f\u0435\u0440\u0435\u043d\u0435\u0441\u0442\u0438 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u0435", None))
        self.pushButton_6.setText(QCoreApplication.translate("reportWindow", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u043a\u043e\u043c\u043d\u0430\u0442\u0443", None))
        self.pushButton_8.setText(QCoreApplication.translate("reportWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0432\u0441\u0451", None))
        self.groupBox.setTitle("")
        self.textEdit_2.setHtml(QCoreApplication.translate("reportWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#3b3b3b;\">\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u044e, \u043c\u043e\u0434\u0435\u043b\u0438, \u0442\u0438\u043f\u0443...</span></p></body></html>", None))
        self.label_66.setText(QCoreApplication.translate("reportWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.label_68.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0438\u043f:", None))
        self.label_64.setText(QCoreApplication.translate("reportWindow", u"\u0424\u0438\u043b\u044c\u0442\u0440\u044b:", None))
        self.label_62.setText(QCoreApplication.translate("reportWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u044d\u0442\u0430\u0436:", None))
        self.label_63.setText(QCoreApplication.translate("reportWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043a\u043e\u043c\u043d\u0430\u0442\u0443:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("reportWindow", u"\u0420\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("reportWindow", u"\u041f\u043e\u043a\u0430\u0437 \u0440\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u044f:", None))
        self.label_50.setText(QCoreApplication.translate("reportWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.label_54.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0438\u043f:", None))
        self.textEdit_3.setHtml(QCoreApplication.translate("reportWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#3b3b3b;\">\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u044e, \u043c\u043e\u0434\u0435\u043b\u0438, \u0442\u0438\u043f\u0443...</span></p></body></html>", None))
        self.label_20.setText(QCoreApplication.translate("reportWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043a\u043e\u043c\u043d\u0430\u0442\u0443:", None))
        self.label_19.setText(QCoreApplication.translate("reportWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u044d\u0442\u0430\u0436:", None))
        self.label_70.setText(QCoreApplication.translate("reportWindow", u"\u0412\u044b\u0431\u043e\u0440 \u0444\u0435\u043b\u0438\u0430\u043b\u0430:", None))
        self.pushButton_14.setText(QCoreApplication.translate("reportWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u043a\u0430 \u043f\u043e\u043b\u043d\u043e\u0439 \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438", None))
        self.pushButton_11.setText(QCoreApplication.translate("reportWindow", u"\u041f\u0435\u0447\u0430\u0442\u044c \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438 \u043f\u043e \u043a\u043e\u043c\u043d\u0430\u0442\u0435", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("reportWindow", u"\u0418\u043d\u0432\u0435\u043d\u0442\u0430\u0440\u0438\u0437\u0430\u0438\u0446\u0438\u044f", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("reportWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u044f:", None))
        self.label_13.setText(QCoreApplication.translate("reportWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435:", None))
        self.lineEdit_5.setText(QCoreApplication.translate("reportWindow", u"\u041f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u0435 \u2116 ", None))
        self.label_14.setText(QCoreApplication.translate("reportWindow", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043e\u0442\u0447\u0435\u0442\u0430:", None))
        self.label_15.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u043f\u0440\u0438\u043a\u0430\u0437\u0430:*", None))
        self.lineEdit_6.setText("")
        self.groupBox_8.setTitle(QCoreApplication.translate("reportWindow", u"\u0412\u044b\u0431\u043e\u0440 \u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u044f:", None))
        self.label_16.setText(QCoreApplication.translate("reportWindow", u"\u0424\u0438\u043b\u0438\u0430\u043b:", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("reportWindow", u"\u041f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u0435 \u043d\u0430 \u0441\u043a\u043b\u0430\u0434", None))
        self.label_26.setText(QCoreApplication.translate("reportWindow", u"Email \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430:", None))
        self.label_25.setText(QCoreApplication.translate("reportWindow", u"\u041f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c(\u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a):", None))
        self.label_24.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430:", None))
        self.label_17.setText(QCoreApplication.translate("reportWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430:", None))
        self.label_30.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u0434\u043e\u043a\u043b\u0430\u0434\u043d\u043e\u0439 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430:", None))
        self.label_29.setText(QCoreApplication.translate("reportWindow", u"\u0418\u041d\u041d \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430:", None))
        self.label_22.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0435\u043b\u0435\u0444\u043e\u043d \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430:", None))
        self.label_23.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u0442\u043e\u0432\u0430\u0440\u043d\u043e\u0439 \u043d\u0430\u043a\u043b\u0430\u0434\u043d\u043e\u0439:", None))
        self.label_33.setText(QCoreApplication.translate("reportWindow", u"\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u044f:", None))
        self.label_31.setText(QCoreApplication.translate("reportWindow", u"\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u044f:", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("reportWindow", u"\u041f\u043e\u0437\u0438\u0446\u0438\u044f \u041f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u0435 :", None))
        self.label_32.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u043f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u044f:", None))
        self.label_28.setText(QCoreApplication.translate("reportWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.label_27.setText(QCoreApplication.translate("reportWindow", u"\u041c\u043e\u0434\u0435\u043b\u044c:", None))
        self.label_36.setText(QCoreApplication.translate("reportWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435:", None))
        self.label_37.setText(QCoreApplication.translate("reportWindow", u"\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c:", None))
        self.label_35.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0438\u043f:", None))
        self.label_40.setText(QCoreApplication.translate("reportWindow", u"\u0421\u0435\u0440\u0438\u0439\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440:", None))
        self.label_39.setText(QCoreApplication.translate("reportWindow", u"\u0418\u043d\u0432\u0435\u043d\u0442\u0440\u0430\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440:", None))
        self.label_42.setText(QCoreApplication.translate("reportWindow", u"\u0426\u0435\u043d\u0430 \u0437\u0430 \u0435\u0434\u0435\u043d\u0438\u0446\u0443:", None))
        self.label_41.setText(QCoreApplication.translate("reportWindow", u"\u0413\u0430\u0440\u0430\u043d\u0442\u0438\u044f:", None))
        self.label_43.setText(QCoreApplication.translate("reportWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e:", None))
        self.label_45.setText(QCoreApplication.translate("reportWindow", u"\u0414\u0430\u0442\u0430 \u043f\u0440\u043e\u0438\u0437\u043e\u0432\u0434\u0441\u0442\u0432\u0430:", None))
        self.label_46.setText(QCoreApplication.translate("reportWindow", u"\u0421\u0440\u043e\u043a \u0433\u043e\u0434\u043d\u043e\u0441\u0442\u0438:*", None))
        self.label_47.setText(QCoreApplication.translate("reportWindow", u"\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435:", None))
        self.label_48.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438:", None))
        self.label_34.setText(QCoreApplication.translate("reportWindow", u"<html><head/><body><p><span style=\" font-size:18pt;\">\u041d\u041e\u0412\u041e\u0415 \u041f\u041e\u0421\u0422\u0423\u041f\u041b\u0415\u041d\u0418\u042f :</span></p></body></html>", None))
        self.label_38.setText(QCoreApplication.translate("reportWindow", u"<html><head/><body><p><span style=\" font-size:18pt;\">\u0411\u0410\u0417\u0410 \u0414\u0410\u041d\u041d\u042b\u0425</span></p><p><br/></p><p><span style=\" font-size:18pt;\"><br/></span></p></body></html>", None))
        self.pushButton_16.setText(QCoreApplication.translate("reportWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u043e\u0437\u0438\u0446\u0438\u044e: >", None))
        self.pushButton_5.setText(QCoreApplication.translate("reportWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0431\u0430\u0437\u0443 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.pushButton_7.setText(QCoreApplication.translate("reportWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.textEdit.setHtml(QCoreApplication.translate("reportWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("reportWindow", u"\u041f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u0435", None))
    # retranslateUi

