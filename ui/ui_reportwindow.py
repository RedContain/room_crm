# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ReportWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
    QDoubleSpinBox, QFormLayout, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpinBox,
    QTabWidget, QTableView, QTableWidget, QTableWidgetItem,
    QTextEdit, QWidget)

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
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tableWidget = QTableWidget(self.tab_2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(915, 50, 541, 746))
        self.label_34 = QLabel(self.tab_2)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setGeometry(QRect(10, 10, 271, 31))
        self.label_34.setStyleSheet(u"font: 28pt \"Segoe UI\";")
        self.label_38 = QLabel(self.tab_2)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setGeometry(QRect(915, 15, 141, 31))
        self.label_38.setStyleSheet(u"font: 28pt \"Segoe UI\";")
        self.pushButton_16 = QPushButton(self.tab_2)
        self.pushButton_16.setObjectName(u"pushButton_16")
        self.pushButton_16.setGeometry(QRect(745, 800, 151, 26))
        self.pushButton_5 = QPushButton(self.tab_2)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(915, 800, 331, 26))
        self.pushButton_7 = QPushButton(self.tab_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(1255, 800, 201, 26))
        self.textEdit = QTextEdit(self.tab_2)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(1055, 15, 396, 26))
        self.formLayoutWidget = QWidget(self.tab_2)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(480, 50, 416, 746))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_37 = QLabel(self.formLayoutWidget)
        self.label_37.setObjectName(u"label_37")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_37)

        self.lineEdit_17 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_17.setObjectName(u"lineEdit_17")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEdit_17)

        self.label_36 = QLabel(self.formLayoutWidget)
        self.label_36.setObjectName(u"label_36")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_36)

        self.lineEdit_16 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_16.setObjectName(u"lineEdit_16")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEdit_16)

        self.label_27 = QLabel(self.formLayoutWidget)
        self.label_27.setObjectName(u"label_27")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_27)

        self.lineEdit_15 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_15.setObjectName(u"lineEdit_15")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lineEdit_15)

        self.label_35 = QLabel(self.formLayoutWidget)
        self.label_35.setObjectName(u"label_35")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_35)

        self.comboBox_9 = QComboBox(self.formLayoutWidget)
        self.comboBox_9.setObjectName(u"comboBox_9")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.comboBox_9)

        self.comboBox_10 = QComboBox(self.formLayoutWidget)
        self.comboBox_10.setObjectName(u"comboBox_10")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.comboBox_10)

        self.label_28 = QLabel(self.formLayoutWidget)
        self.label_28.setObjectName(u"label_28")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_28)

        self.label_32 = QLabel(self.formLayoutWidget)
        self.label_32.setObjectName(u"label_32")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_32)

        self.lineEdit_14 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_14.setObjectName(u"lineEdit_14")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEdit_14)

        self.label_40 = QLabel(self.formLayoutWidget)
        self.label_40.setObjectName(u"label_40")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_40)

        self.lineEdit_18 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_18.setObjectName(u"lineEdit_18")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.lineEdit_18)

        self.lineEdit_19 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_19.setObjectName(u"lineEdit_19")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.lineEdit_19)

        self.label_39 = QLabel(self.formLayoutWidget)
        self.label_39.setObjectName(u"label_39")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.label_39)

        self.label_45 = QLabel(self.formLayoutWidget)
        self.label_45.setObjectName(u"label_45")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.label_45)

        self.dateEdit = QDateEdit(self.formLayoutWidget)
        self.dateEdit.setObjectName(u"dateEdit")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.dateEdit)

        self.dateEdit_2 = QDateEdit(self.formLayoutWidget)
        self.dateEdit_2.setObjectName(u"dateEdit_2")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.dateEdit_2)

        self.label_46 = QLabel(self.formLayoutWidget)
        self.label_46.setObjectName(u"label_46")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.label_46)

        self.label_48 = QLabel(self.formLayoutWidget)
        self.label_48.setObjectName(u"label_48")

        self.formLayout.setWidget(13, QFormLayout.ItemRole.LabelRole, self.label_48)

        self.plainTextEdit_3 = QPlainTextEdit(self.formLayoutWidget)
        self.plainTextEdit_3.setObjectName(u"plainTextEdit_3")

        self.formLayout.setWidget(13, QFormLayout.ItemRole.FieldRole, self.plainTextEdit_3)

        self.label_47 = QLabel(self.formLayoutWidget)
        self.label_47.setObjectName(u"label_47")

        self.formLayout.setWidget(14, QFormLayout.ItemRole.LabelRole, self.label_47)

        self.plainTextEdit_4 = QPlainTextEdit(self.formLayoutWidget)
        self.plainTextEdit_4.setObjectName(u"plainTextEdit_4")

        self.formLayout.setWidget(14, QFormLayout.ItemRole.FieldRole, self.plainTextEdit_4)

        self.label_43 = QLabel(self.formLayoutWidget)
        self.label_43.setObjectName(u"label_43")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.label_43)

        self.spinBox_2 = QSpinBox(self.formLayoutWidget)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMinimum(0)
        self.spinBox_2.setMaximum(999999999)

        self.formLayout.setWidget(10, QFormLayout.ItemRole.FieldRole, self.spinBox_2)

        self.doubleSpinBox = QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMaximum(10000000000000000.000000000000000)

        self.formLayout.setWidget(11, QFormLayout.ItemRole.FieldRole, self.doubleSpinBox)

        self.label_42 = QLabel(self.formLayoutWidget)
        self.label_42.setObjectName(u"label_42")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.label_42)

        self.label_41 = QLabel(self.formLayoutWidget)
        self.label_41.setObjectName(u"label_41")

        self.formLayout.setWidget(12, QFormLayout.ItemRole.LabelRole, self.label_41)

        self.spinBox_4 = QSpinBox(self.formLayoutWidget)
        self.spinBox_4.setObjectName(u"spinBox_4")
        self.spinBox_4.setMaximum(999999999)

        self.formLayout.setWidget(12, QFormLayout.ItemRole.FieldRole, self.spinBox_4)

        self.line = QFrame(self.tab_2)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(453, 50, 16, 541))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.formLayoutWidget_2 = QWidget(self.tab_2)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(10, 50, 436, 541))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_13 = QLabel(self.formLayoutWidget_2)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_13)

        self.lineEdit_5 = QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEdit_5)

        self.label_14 = QLabel(self.formLayoutWidget_2)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_14)

        self.textEdit_4 = QTextEdit(self.formLayoutWidget_2)
        self.textEdit_4.setObjectName(u"textEdit_4")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.textEdit_4)

        self.label_15 = QLabel(self.formLayoutWidget_2)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_15)

        self.lineEdit_6 = QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEdit_6)

        self.label_30 = QLabel(self.formLayoutWidget_2)
        self.label_30.setObjectName(u"label_30")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_30)

        self.lineEdit_2 = QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lineEdit_2)

        self.label_16 = QLabel(self.formLayoutWidget_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMaximumSize(QSize(51, 22))
        self.label_16.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_16.setAutoFillBackground(False)

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_16)

        self.comboBox_5 = QComboBox(self.formLayoutWidget_2)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.FieldRole, self.comboBox_5)

        self.label_31 = QLabel(self.formLayoutWidget_2)
        self.label_31.setObjectName(u"label_31")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_31)

        self.dateTimeEdit = QDateTimeEdit(self.formLayoutWidget_2)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.FieldRole, self.dateTimeEdit)

        self.label_17 = QLabel(self.formLayoutWidget_2)
        self.label_17.setObjectName(u"label_17")

        self.formLayout_2.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_17)

        self.lineEdit_7 = QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.formLayout_2.setWidget(6, QFormLayout.ItemRole.FieldRole, self.lineEdit_7)

        self.label_29 = QLabel(self.formLayoutWidget_2)
        self.label_29.setObjectName(u"label_29")

        self.formLayout_2.setWidget(7, QFormLayout.ItemRole.LabelRole, self.label_29)

        self.lineEdit_8 = QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_8.setObjectName(u"lineEdit_8")

        self.formLayout_2.setWidget(7, QFormLayout.ItemRole.FieldRole, self.lineEdit_8)

        self.label_22 = QLabel(self.formLayoutWidget_2)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_2.setWidget(8, QFormLayout.ItemRole.LabelRole, self.label_22)

        self.lineEdit_9 = QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.formLayout_2.setWidget(8, QFormLayout.ItemRole.FieldRole, self.lineEdit_9)

        self.label_26 = QLabel(self.formLayoutWidget_2)
        self.label_26.setObjectName(u"label_26")

        self.formLayout_2.setWidget(9, QFormLayout.ItemRole.LabelRole, self.label_26)

        self.lineEdit_10 = QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_10.setObjectName(u"lineEdit_10")

        self.formLayout_2.setWidget(9, QFormLayout.ItemRole.FieldRole, self.lineEdit_10)

        self.label_23 = QLabel(self.formLayoutWidget_2)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_2.setWidget(10, QFormLayout.ItemRole.LabelRole, self.label_23)

        self.lineEdit_12 = QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_12.setObjectName(u"lineEdit_12")

        self.formLayout_2.setWidget(10, QFormLayout.ItemRole.FieldRole, self.lineEdit_12)

        self.label_24 = QLabel(self.formLayoutWidget_2)
        self.label_24.setObjectName(u"label_24")

        self.formLayout_2.setWidget(11, QFormLayout.ItemRole.LabelRole, self.label_24)

        self.lineEdit_13 = QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_13.setObjectName(u"lineEdit_13")

        self.formLayout_2.setWidget(11, QFormLayout.ItemRole.FieldRole, self.lineEdit_13)

        self.label_25 = QLabel(self.formLayoutWidget_2)
        self.label_25.setObjectName(u"label_25")

        self.formLayout_2.setWidget(12, QFormLayout.ItemRole.LabelRole, self.label_25)

        self.comboBox_8 = QComboBox(self.formLayoutWidget_2)
        self.comboBox_8.setObjectName(u"comboBox_8")

        self.formLayout_2.setWidget(12, QFormLayout.ItemRole.FieldRole, self.comboBox_8)

        self.label_33 = QLabel(self.formLayoutWidget_2)
        self.label_33.setObjectName(u"label_33")

        self.formLayout_2.setWidget(13, QFormLayout.ItemRole.LabelRole, self.label_33)

        self.plainTextEdit = QPlainTextEdit(self.formLayoutWidget_2)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.formLayout_2.setWidget(13, QFormLayout.ItemRole.FieldRole, self.plainTextEdit)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tableView_2 = QTableView(self.tab_5)
        self.tableView_2.setObjectName(u"tableView_2")
        self.tableView_2.setGeometry(QRect(335, 25, 516, 646))
        self.pushButton_8 = QPushButton(self.tab_5)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(1330, 680, 121, 26))
        self.pushButton_15 = QPushButton(self.tab_5)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setGeometry(QRect(860, 205, 81, 26))
        self.pushButton_6 = QPushButton(self.tab_5)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(955, 680, 121, 26))
        self.tableView_3 = QTableView(self.tab_5)
        self.tableView_3.setObjectName(u"tableView_3")
        self.tableView_3.setGeometry(QRect(955, 25, 496, 646))
        self.pushButton_17 = QPushButton(self.tab_5)
        self.pushButton_17.setObjectName(u"pushButton_17")
        self.pushButton_17.setGeometry(QRect(860, 260, 81, 26))
        self.formLayoutWidget_3 = QWidget(self.tab_5)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(14, 25, 311, 406))
        self.formLayout_3 = QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_59 = QLabel(self.formLayoutWidget_3)
        self.label_59.setObjectName(u"label_59")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_59)

        self.lineEdit_23 = QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_23.setObjectName(u"lineEdit_23")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEdit_23)

        self.label_60 = QLabel(self.formLayoutWidget_3)
        self.label_60.setObjectName(u"label_60")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_60)

        self.textEdit_5 = QTextEdit(self.formLayoutWidget_3)
        self.textEdit_5.setObjectName(u"textEdit_5")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.textEdit_5)

        self.label_61 = QLabel(self.formLayoutWidget_3)
        self.label_61.setObjectName(u"label_61")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_61)

        self.lineEdit_24 = QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_24.setObjectName(u"lineEdit_24")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEdit_24)

        self.label_56 = QLabel(self.formLayoutWidget_3)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setMaximumSize(QSize(51, 22))
        self.label_56.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_56.setAutoFillBackground(False)

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_56)

        self.comboBox_14 = QComboBox(self.formLayoutWidget_3)
        self.comboBox_14.setObjectName(u"comboBox_14")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.FieldRole, self.comboBox_14)

        self.label_49 = QLabel(self.formLayoutWidget_3)
        self.label_49.setObjectName(u"label_49")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_49)

        self.comboBox_13 = QComboBox(self.formLayoutWidget_3)
        self.comboBox_13.setObjectName(u"comboBox_13")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.FieldRole, self.comboBox_13)

        self.label_62 = QLabel(self.formLayoutWidget_3)
        self.label_62.setObjectName(u"label_62")

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_62)

        self.spinBox_6 = QSpinBox(self.formLayoutWidget_3)
        self.spinBox_6.setObjectName(u"spinBox_6")

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.FieldRole, self.spinBox_6)

        self.label_63 = QLabel(self.formLayoutWidget_3)
        self.label_63.setObjectName(u"label_63")

        self.formLayout_3.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_63)

        self.comboBox_16 = QComboBox(self.formLayoutWidget_3)
        self.comboBox_16.setObjectName(u"comboBox_16")

        self.formLayout_3.setWidget(6, QFormLayout.ItemRole.FieldRole, self.comboBox_16)

        self.label_68 = QLabel(self.formLayoutWidget_3)
        self.label_68.setObjectName(u"label_68")

        self.formLayout_3.setWidget(7, QFormLayout.ItemRole.LabelRole, self.label_68)

        self.comboBox_18 = QComboBox(self.formLayoutWidget_3)
        self.comboBox_18.setObjectName(u"comboBox_18")

        self.formLayout_3.setWidget(7, QFormLayout.ItemRole.FieldRole, self.comboBox_18)

        self.label_66 = QLabel(self.formLayoutWidget_3)
        self.label_66.setObjectName(u"label_66")

        self.formLayout_3.setWidget(8, QFormLayout.ItemRole.LabelRole, self.label_66)

        self.comboBox_17 = QComboBox(self.formLayoutWidget_3)
        self.comboBox_17.setObjectName(u"comboBox_17")

        self.formLayout_3.setWidget(8, QFormLayout.ItemRole.FieldRole, self.comboBox_17)

        self.gridLayout_32 = QGridLayout()
        self.gridLayout_32.setObjectName(u"gridLayout_32")

        self.formLayout_3.setLayout(9, QFormLayout.ItemRole.LabelRole, self.gridLayout_32)

        self.textEdit_2 = QTextEdit(self.tab_5)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(15, 435, 311, 26))
        self.tabWidget.addTab(self.tab_5, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.widget_6 = QWidget(self.tab)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setGeometry(QRect(10, 10, 1876, 911))
        self.tableView = QTableView(self.widget_6)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(330, 40, 991, 526))
        self.pushButton_14 = QPushButton(self.widget_6)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setGeometry(QRect(115, 175, 206, 26))
        self.pushButton_11 = QPushButton(self.widget_6)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(115, 205, 206, 26))
        self.textEdit_3 = QTextEdit(self.widget_6)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setGeometry(QRect(330, 10, 276, 26))
        self.formLayoutWidget_4 = QWidget(self.widget_6)
        self.formLayoutWidget_4.setObjectName(u"formLayoutWidget_4")
        self.formLayoutWidget_4.setGeometry(QRect(10, 10, 311, 161))
        self.formLayout_4 = QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_70 = QLabel(self.formLayoutWidget_4)
        self.label_70.setObjectName(u"label_70")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_70)

        self.comboBox_19 = QComboBox(self.formLayoutWidget_4)
        self.comboBox_19.setObjectName(u"comboBox_19")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboBox_19)

        self.label_19 = QLabel(self.formLayoutWidget_4)
        self.label_19.setObjectName(u"label_19")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_19)

        self.spinBox_3 = QSpinBox(self.formLayoutWidget_4)
        self.spinBox_3.setObjectName(u"spinBox_3")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spinBox_3)

        self.label_20 = QLabel(self.formLayoutWidget_4)
        self.label_20.setObjectName(u"label_20")

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_20)

        self.comboBox_7 = QComboBox(self.formLayoutWidget_4)
        self.comboBox_7.setObjectName(u"comboBox_7")

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.FieldRole, self.comboBox_7)

        self.label_50 = QLabel(self.formLayoutWidget_4)
        self.label_50.setObjectName(u"label_50")

        self.formLayout_4.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_50)

        self.comboBox_12 = QComboBox(self.formLayoutWidget_4)
        self.comboBox_12.setObjectName(u"comboBox_12")

        self.formLayout_4.setWidget(3, QFormLayout.ItemRole.FieldRole, self.comboBox_12)

        self.label_54 = QLabel(self.formLayoutWidget_4)
        self.label_54.setObjectName(u"label_54")

        self.formLayout_4.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_54)

        self.comboBox_11 = QComboBox(self.formLayoutWidget_4)
        self.comboBox_11.setObjectName(u"comboBox_11")

        self.formLayout_4.setWidget(4, QFormLayout.ItemRole.FieldRole, self.comboBox_11)

        self.tabWidget.addTab(self.tab, "")
        reportWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(reportWindow)

        self.tabWidget.setCurrentIndex(2)


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
        self.label_34.setText(QCoreApplication.translate("reportWindow", u"<html><head/><body><p><span style=\" font-size:18pt;\">\u041d\u041e\u0412\u041e\u0415 \u041f\u041e\u0421\u0422\u0423\u041f\u041b\u0415\u041d\u0418\u042f :</span></p></body></html>", None))
        self.label_38.setText(QCoreApplication.translate("reportWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">\u0411\u0410\u0417\u0410 \u0414\u0410\u041d\u041d\u042b\u0425</span></p><p><span style=\" font-size:14pt;\"><br/></span></p><p><span style=\" font-size:14pt;\"><br/></span></p></body></html>", None))
        self.pushButton_16.setText(QCoreApplication.translate("reportWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None))
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
        self.label_37.setText(QCoreApplication.translate("reportWindow", u"\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c:", None))
        self.label_36.setText(QCoreApplication.translate("reportWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435:", None))
        self.label_27.setText(QCoreApplication.translate("reportWindow", u"\u041c\u043e\u0434\u0435\u043b\u044c:", None))
        self.label_35.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0438\u043f:", None))
        self.label_28.setText(QCoreApplication.translate("reportWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.label_32.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u043f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u044f:", None))
        self.label_40.setText(QCoreApplication.translate("reportWindow", u"\u0421\u0435\u0440\u0438\u0439\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440:", None))
        self.label_39.setText(QCoreApplication.translate("reportWindow", u"\u0418\u043d\u0432\u0435\u043d\u0442\u0440\u0430\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440:", None))
        self.label_45.setText(QCoreApplication.translate("reportWindow", u"\u0414\u0430\u0442\u0430 \u043f\u0440\u043e\u0438\u0437\u043e\u0432\u0434\u0441\u0442\u0432\u0430:", None))
        self.label_46.setText(QCoreApplication.translate("reportWindow", u"\u0421\u0440\u043e\u043a \u0433\u043e\u0434\u043d\u043e\u0441\u0442\u0438:*", None))
        self.label_48.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438:", None))
        self.label_47.setText(QCoreApplication.translate("reportWindow", u"\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435:", None))
        self.label_43.setText(QCoreApplication.translate("reportWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e:", None))
        self.label_42.setText(QCoreApplication.translate("reportWindow", u"\u0426\u0435\u043d\u0430 \u0437\u0430 \u0435\u0434\u0435\u043d\u0438\u0446\u0443:", None))
        self.label_41.setText(QCoreApplication.translate("reportWindow", u"\u0413\u0430\u0440\u0430\u043d\u0442\u0438\u044f:", None))
        self.label_13.setText(QCoreApplication.translate("reportWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435:", None))
        self.lineEdit_5.setText(QCoreApplication.translate("reportWindow", u"\u041f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u0435 \u2116 ", None))
        self.label_14.setText(QCoreApplication.translate("reportWindow", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043e\u0442\u0447\u0435\u0442\u0430:", None))
        self.label_15.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u043f\u0440\u0438\u043a\u0430\u0437\u0430:*", None))
        self.lineEdit_6.setText("")
        self.label_30.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u0434\u043e\u043a\u043b\u0430\u0434\u043d\u043e\u0439 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430:", None))
        self.label_16.setText(QCoreApplication.translate("reportWindow", u"\u0424\u0438\u043b\u0438\u0430\u043b:", None))
        self.label_31.setText(QCoreApplication.translate("reportWindow", u"\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u044f:", None))
        self.label_17.setText(QCoreApplication.translate("reportWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430:", None))
        self.label_29.setText(QCoreApplication.translate("reportWindow", u"\u0418\u041d\u041d \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430:", None))
        self.label_22.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0435\u043b\u0435\u0444\u043e\u043d \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430:", None))
        self.label_26.setText(QCoreApplication.translate("reportWindow", u"Email \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430:", None))
        self.label_23.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u0442\u043e\u0432\u0430\u0440\u043d\u043e\u0439 \u043d\u0430\u043a\u043b\u0430\u0434\u043d\u043e\u0439:", None))
        self.label_24.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430:", None))
        self.label_25.setText(QCoreApplication.translate("reportWindow", u"\u041f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c(\u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a):", None))
        self.label_33.setText(QCoreApplication.translate("reportWindow", u"\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u044f:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("reportWindow", u"\u041f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u0435", None))
        self.pushButton_8.setText(QCoreApplication.translate("reportWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0432\u0441\u0451", None))
        self.pushButton_15.setText(QCoreApplication.translate("reportWindow", u">>>", None))
        self.pushButton_6.setText(QCoreApplication.translate("reportWindow", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u043a\u043e\u043c\u043d\u0430\u0442\u0443", None))
        self.pushButton_17.setText(QCoreApplication.translate("reportWindow", u"<<<", None))
        self.label_59.setText(QCoreApplication.translate("reportWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 :", None))
        self.label_60.setText(QCoreApplication.translate("reportWindow", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435:", None))
        self.label_61.setText(QCoreApplication.translate("reportWindow", u"\u041d\u043e\u043c\u0435\u0440 \u043f\u0440\u0438\u043a\u0430\u0437\u0430:*", None))
        self.lineEdit_24.setText("")
        self.label_56.setText(QCoreApplication.translate("reportWindow", u"\u0424\u0438\u043b\u0438\u0430\u043b:", None))
        self.label_49.setText(QCoreApplication.translate("reportWindow", u"\u0424\u0418\u041e:", None))
        self.label_62.setText(QCoreApplication.translate("reportWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u044d\u0442\u0430\u0436:", None))
        self.label_63.setText(QCoreApplication.translate("reportWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043a\u043e\u043c\u043d\u0430\u0442\u0443:", None))
        self.label_68.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0438\u043f:", None))
        self.label_66.setText(QCoreApplication.translate("reportWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.textEdit_2.setHtml(QCoreApplication.translate("reportWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#3b3b3b;\">\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u044e, \u043c\u043e\u0434\u0435\u043b\u0438, \u0442\u0438\u043f\u0443...</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("reportWindow", u"\u0420\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435", None))
        self.pushButton_14.setText(QCoreApplication.translate("reportWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u043a\u0430 \u043f\u043e\u043b\u043d\u043e\u0439 \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438", None))
        self.pushButton_11.setText(QCoreApplication.translate("reportWindow", u"\u041f\u0435\u0447\u0430\u0442\u044c \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438 \u043f\u043e \u043a\u043e\u043c\u043d\u0430\u0442\u0435", None))
        self.textEdit_3.setHtml(QCoreApplication.translate("reportWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#3b3b3b;\">\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u044e, \u043c\u043e\u0434\u0435\u043b\u0438, \u0442\u0438\u043f\u0443...</span></p></body></html>", None))
        self.label_70.setText(QCoreApplication.translate("reportWindow", u"\u0412\u044b\u0431\u043e\u0440 \u0444\u0435\u043b\u0438\u0430\u043b\u0430:", None))
        self.label_19.setText(QCoreApplication.translate("reportWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u044d\u0442\u0430\u0436:", None))
        self.label_20.setText(QCoreApplication.translate("reportWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043a\u043e\u043c\u043d\u0430\u0442\u0443:", None))
        self.label_50.setText(QCoreApplication.translate("reportWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.label_54.setText(QCoreApplication.translate("reportWindow", u"\u0422\u0438\u043f:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("reportWindow", u"\u0418\u043d\u0432\u0435\u043d\u0442\u0430\u0440\u0438\u0437\u0430\u0438\u0446\u0438\u044f", None))
    # retranslateUi

