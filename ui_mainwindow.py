# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QLabel, QLayout, QMainWindow,
    QPushButton, QSizePolicy, QSpinBox, QStatusBar,
    QVBoxLayout, QWidget)

from carpetview import CarpetView
from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1127, 810)
        self.actionOpen_ECG = QAction(MainWindow)
        self.actionOpen_ECG.setObjectName(u"actionOpen_ECG")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.carpetView = CarpetView(self.centralwidget)
        self.carpetView.setObjectName(u"carpetView")
        self.carpetView.setEnabled(True)

        self.gridLayout.addWidget(self.carpetView, 0, 0, 1, 1)

        self.signalView = PlotWidget(self.centralwidget)
        self.signalView.setObjectName(u"signalView")

        self.gridLayout.addWidget(self.signalView, 1, 0, 1, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.openPushButton = QPushButton(self.groupBox)
        self.openPushButton.setObjectName(u"openPushButton")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.openPushButton)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.r1spinBox = QSpinBox(self.groupBox)
        self.r1spinBox.setObjectName(u"r1spinBox")
        self.r1spinBox.setSingleStep(60)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.r1spinBox)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label)

        self.r2spinBox = QSpinBox(self.groupBox)
        self.r2spinBox.setObjectName(u"r2spinBox")
        self.r2spinBox.setMaximum(256)
        self.r2spinBox.setSingleStep(60)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.r2spinBox)

        self.updateRangePushButton = QPushButton(self.groupBox)
        self.updateRangePushButton.setObjectName(u"updateRangePushButton")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.SpanningRole, self.updateRangePushButton)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.leadComboBox = QComboBox(self.groupBox)
        self.leadComboBox.setObjectName(u"leadComboBox")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.leadComboBox)

        self.rSourceLeadComboBox = QComboBox(self.groupBox)
        self.rSourceLeadComboBox.setObjectName(u"rSourceLeadComboBox")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.rSourceLeadComboBox)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.cmapComboBox = QComboBox(self.groupBox)
        self.cmapComboBox.addItem("")
        self.cmapComboBox.addItem("")
        self.cmapComboBox.addItem("")
        self.cmapComboBox.addItem("")
        self.cmapComboBox.addItem("")
        self.cmapComboBox.setObjectName(u"cmapComboBox")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.cmapComboBox)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_2)


        self.verticalLayout.addLayout(self.formLayout)

        self.themeComboBox = QComboBox(self.groupBox)
        self.themeComboBox.addItem("")
        self.themeComboBox.addItem("")
        self.themeComboBox.setObjectName(u"themeComboBox")

        self.verticalLayout.addWidget(self.themeComboBox)

        self.exportPushButton = QPushButton(self.groupBox)
        self.exportPushButton.setObjectName(u"exportPushButton")

        self.verticalLayout.addWidget(self.exportPushButton)


        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.gridLayout.setRowStretch(0, 3)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setColumnStretch(0, 10)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnMinimumWidth(1, 180)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Dywaniki", None))
        self.actionOpen_ECG.setText(QCoreApplication.translate("MainWindow", u"&Open ECG", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.openPushButton.setText(QCoreApplication.translate("MainWindow", u"Open file", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"first R", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"beats", None))
        self.updateRangePushButton.setText(QCoreApplication.translate("MainWindow", u"Update range", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Lead", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"R source", None))
        self.cmapComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"jet", None))
        self.cmapComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"seismic", None))
        self.cmapComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"bwr", None))
        self.cmapComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"gray", None))
        self.cmapComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"gray_r", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Color map", None))
        self.themeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"dark", None))
        self.themeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"light", None))

        self.exportPushButton.setText(QCoreApplication.translate("MainWindow", u"Export image", None))
    # retranslateUi

