# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plane.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGridLayout,
    QHeaderView, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QTabWidget,
    QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1922, 824)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 80, 1901, 721))
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.label_6 = QLabel(self.tab_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 50, 101, 21))
        self.label_7 = QLabel(self.tab_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 15, 101, 21))
        self.spinBox_2 = QSpinBox(self.tab_3)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setGeometry(QRect(110, 50, 141, 26))
        self.comboBox_2 = QComboBox(self.tab_3)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(110, 10, 381, 31))
        self.pushButton_6 = QPushButton(self.tab_3)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(20, 660, 201, 26))
        self.pushButton_7 = QPushButton(self.tab_3)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(230, 660, 241, 26))
        self.graphicsView_2 = QGraphicsView(self.tab_3)
        self.graphicsView_2.setObjectName(u"graphicsView_2")
        self.graphicsView_2.setGeometry(QRect(10, 90, 1871, 561))
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.label_2 = QLabel(self.tab_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 15, 101, 21))
        self.comboBox = QComboBox(self.tab_4)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(110, 10, 381, 31))
        self.label_3 = QLabel(self.tab_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 50, 101, 21))
        self.spinBox = QSpinBox(self.tab_4)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(110, 50, 141, 26))
        self.gridLayoutWidget = QWidget(self.tab_4)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 80, 241, 121))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)

        self.pushButton_3 = QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"red")

        self.gridLayout.addWidget(self.pushButton_3, 2, 0, 1, 1)

        self.tableView = QTableView(self.tab_4)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(500, 510, 721, 171))
        self.graphicsView = QGraphicsView(self.tab_4)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(500, 10, 1381, 491))
        self.pushButton_8 = QPushButton(self.tab_4)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(10, 210, 241, 31))
        self.tabWidget.addTab(self.tab_4, "")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 231, 41))
        font = QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>1321321</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u043e\u0440 \u044d\u0442\u0430\u0436\u0430:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u043e\u0440 \u0444\u0438\u043b\u0438\u0430\u043b\u0430:", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u0432\u044b\u0433\u0440\u0443\u0437\u0438\u0442\u044c .pdf \u0432\u0441\u0435\u0433\u043e \u0444\u0438\u043b\u0438\u0430\u043b\u0430", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u0432\u044b\u0433\u0440\u0443\u0437\u0438\u0442\u044c pdf. \u043a\u043e\u043d\u043a\u0440\u0435\u0442\u043d\u043e\u0433\u043e \u044d\u0442\u043e\u0433\u043e \u044d\u0442\u0430\u0436\u0430", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u043e\u0440 \u0444\u0438\u043b\u0438\u0430\u043b\u0430:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u043e\u0440 \u044d\u0442\u0430\u0436\u0430:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0441\u0445\u0435\u043c\u0443", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441\u0445\u0435\u043c\u0443", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0441\u0445\u0435\u043c\u0443", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u041e\u041a\u0410\u0417 \u0421\u0425\u0415\u041c\u042b", None))
    # retranslateUi

