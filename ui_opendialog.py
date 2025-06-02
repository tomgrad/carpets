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
    QDialogButtonBox, QLabel, QSizePolicy, QTimeEdit,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(362, 267)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(180, 220, 171, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 120, 141, 17))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 160, 151, 17))
        self.durationLabel = QLabel(Dialog)
        self.durationLabel.setObjectName(u"durationLabel")
        self.durationLabel.setGeometry(QRect(30, 40, 301, 17))
        self.preview = QCheckBox(Dialog)
        self.preview.setObjectName(u"preview")
        self.preview.setGeometry(QRect(30, 80, 121, 23))
        self.durationTimeEdit = QTimeEdit(Dialog)
        self.durationTimeEdit.setObjectName(u"durationTimeEdit")
        self.durationTimeEdit.setGeometry(QRect(200, 110, 81, 32))
        self.durationTimeEdit.setTime(QTime(1, 0, 0))
        self.startTimeEdit = QTimeEdit(Dialog)
        self.startTimeEdit.setObjectName(u"startTimeEdit")
        self.startTimeEdit.setGeometry(QRect(200, 150, 81, 32))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Import only (HH:mm)", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"starting from (HH:mm)", None))
        self.durationLabel.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.preview.setText(QCoreApplication.translate("Dialog", u"quick preview", None))
    # retranslateUi

