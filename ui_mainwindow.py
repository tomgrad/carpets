# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QButtonGroup, QCheckBox,
    QComboBox, QDoubleSpinBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QMainWindow, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QSplitter, QStatusBar, QVBoxLayout, QWidget)

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
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.carpetView = CarpetView(self.splitter)
        self.carpetView.setObjectName(u"carpetView")
        self.carpetView.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.carpetView.sizePolicy().hasHeightForWidth())
        self.carpetView.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.carpetView)
        self.signalView = PlotWidget(self.splitter)
        self.signalView.setObjectName(u"signalView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.signalView.sizePolicy().hasHeightForWidth())
        self.signalView.setSizePolicy(sizePolicy1)
        self.signalView.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.splitter.addWidget(self.signalView)

        self.horizontalLayout.addWidget(self.splitter)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.openPushButton = QPushButton(self.groupBox)
        self.openPushButton.setObjectName(u"openPushButton")
        self.openPushButton.setEnabled(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.openPushButton)

        self.fixedHeightCheckBox = QCheckBox(self.groupBox)
        self.fixedHeightCheckBox.setObjectName(u"fixedHeightCheckBox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.fixedHeightCheckBox)

        self.fixedHeightSpinBox = QSpinBox(self.groupBox)
        self.fixedHeightSpinBox.setObjectName(u"fixedHeightSpinBox")
        self.fixedHeightSpinBox.setMinimum(10)
        self.fixedHeightSpinBox.setMaximum(1000000)
        self.fixedHeightSpinBox.setSingleStep(50)
        self.fixedHeightSpinBox.setValue(250)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.fixedHeightSpinBox)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.leadComboBox = QComboBox(self.groupBox)
        self.leadComboBox.setObjectName(u"leadComboBox")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.leadComboBox)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.rSourceLeadComboBox = QComboBox(self.groupBox)
        self.rSourceLeadComboBox.setObjectName(u"rSourceLeadComboBox")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.rSourceLeadComboBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(8, QFormLayout.ItemRole.FieldRole, self.verticalSpacer)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.cmapComboBox = QComboBox(self.groupBox)
        self.cmapComboBox.addItem("")
        self.cmapComboBox.addItem("")
        self.cmapComboBox.addItem("")
        self.cmapComboBox.addItem("")
        self.cmapComboBox.addItem("")
        self.cmapComboBox.addItem("")
        self.cmapComboBox.setObjectName(u"cmapComboBox")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.cmapComboBox)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.label)

        self.fontSizeSpinBox = QSpinBox(self.groupBox)
        self.fontSizeSpinBox.setObjectName(u"fontSizeSpinBox")
        self.fontSizeSpinBox.setMinimum(5)
        self.fontSizeSpinBox.setMaximum(36)
        self.fontSizeSpinBox.setValue(10)

        self.formLayout.setWidget(10, QFormLayout.ItemRole.FieldRole, self.fontSizeSpinBox)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.themeComboBox = QComboBox(self.groupBox)
        self.themeComboBox.addItem("")
        self.themeComboBox.addItem("")
        self.themeComboBox.setObjectName(u"themeComboBox")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.FieldRole, self.themeComboBox)

        self.lineWidthSpinBox = QSpinBox(self.groupBox)
        self.lineWidthSpinBox.setObjectName(u"lineWidthSpinBox")
        self.lineWidthSpinBox.setMinimum(1)
        self.lineWidthSpinBox.setMaximum(5)

        self.formLayout.setWidget(12, QFormLayout.ItemRole.FieldRole, self.lineWidthSpinBox)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(12, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.autolevelsPushButton = QPushButton(self.groupBox)
        self.autolevelsPushButton.setObjectName(u"autolevelsPushButton")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.autolevelsPushButton)

        self.autolevelsSpinBox = QDoubleSpinBox(self.groupBox)
        self.autolevelsSpinBox.setObjectName(u"autolevelsSpinBox")
        self.autolevelsSpinBox.setDecimals(1)
        self.autolevelsSpinBox.setMaximum(50.000000000000000)
        self.autolevelsSpinBox.setSingleStep(0.500000000000000)
        self.autolevelsSpinBox.setValue(1.000000000000000)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.autolevelsSpinBox)

        self.bpmRadioButton = QRadioButton(self.groupBox)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.bpmRadioButton)
        self.bpmRadioButton.setObjectName(u"bpmRadioButton")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.bpmRadioButton)

        self.msRadioButton = QRadioButton(self.groupBox)
        self.buttonGroup.addButton(self.msRadioButton)
        self.msRadioButton.setObjectName(u"msRadioButton")
        self.msRadioButton.setChecked(True)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.msRadioButton)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(5, QFormLayout.ItemRole.FieldRole, self.verticalSpacer_2)


        self.verticalLayout.addLayout(self.formLayout)

        self.exportImagePushButton = QPushButton(self.groupBox)
        self.exportImagePushButton.setObjectName(u"exportImagePushButton")

        self.verticalLayout.addWidget(self.exportImagePushButton)


        self.horizontalLayout.addWidget(self.groupBox)

        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 1)
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
        self.fixedHeightCheckBox.setText(QCoreApplication.translate("MainWindow", u"fixed height", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Lead", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"R source", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Color map", None))
        self.cmapComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"jet", None))
        self.cmapComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"turbo", None))
        self.cmapComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"seismic", None))
        self.cmapComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"bwr", None))
        self.cmapComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"gray", None))
        self.cmapComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"gray_r", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"Font size", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Theme", None))
        self.themeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"dark", None))
        self.themeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"light", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Line width", None))
#if QT_CONFIG(tooltip)
        self.autolevelsPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"Cut-off top and bottom percentile", None))
#endif // QT_CONFIG(tooltip)
        self.autolevelsPushButton.setText(QCoreApplication.translate("MainWindow", u"Auto-levels", None))
        self.bpmRadioButton.setText(QCoreApplication.translate("MainWindow", u"bpm", None))
        self.msRadioButton.setText(QCoreApplication.translate("MainWindow", u"ms", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"x scale units", None))
        self.exportImagePushButton.setText(QCoreApplication.translate("MainWindow", u"Export image", None))
    # retranslateUi

