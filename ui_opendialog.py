# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'opendialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QLabel, QSizePolicy, QSpinBox,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(277, 229)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(90, 190, 171, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.durationMinutes = QSpinBox(Dialog)
        self.durationMinutes.setObjectName(u"durationMinutes")
        self.durationMinutes.setGeometry(QRect(110, 110, 91, 26))
        self.durationMinutes.setMinimum(1)
        self.durationMinutes.setSingleStep(30)
        self.durationMinutes.setValue(30)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 120, 81, 17))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(210, 120, 54, 17))
        self.fromMinutes = QSpinBox(Dialog)
        self.fromMinutes.setObjectName(u"fromMinutes")
        self.fromMinutes.setGeometry(QRect(110, 150, 91, 26))
        self.fromMinutes.setSingleStep(30)
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 160, 81, 17))
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(210, 160, 54, 17))
        self.durationLabel = QLabel(Dialog)
        self.durationLabel.setObjectName(u"durationLabel")
        self.durationLabel.setGeometry(QRect(30, 40, 301, 17))
        self.preview = QCheckBox(Dialog)
        self.preview.setObjectName(u"preview")
        self.preview.setGeometry(QRect(30, 80, 121, 23))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Import only", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"minutes", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"starting from", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"minutes", None))
        self.durationLabel.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.preview.setText(QCoreApplication.translate("Dialog", u"quick preview", None))
    # retranslateUi

