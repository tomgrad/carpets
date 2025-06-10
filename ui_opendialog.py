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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGroupBox, QLabel, QRadioButton, QSizePolicy,
    QTimeEdit, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(333, 373)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(120, 330, 171, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 250, 141, 17))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 290, 151, 17))
        self.durationLabel = QLabel(Dialog)
        self.durationLabel.setObjectName(u"durationLabel")
        self.durationLabel.setGeometry(QRect(30, 40, 301, 17))
        self.durationTimeEdit = QTimeEdit(Dialog)
        self.durationTimeEdit.setObjectName(u"durationTimeEdit")
        self.durationTimeEdit.setEnabled(False)
        self.durationTimeEdit.setGeometry(QRect(210, 240, 81, 32))
        self.durationTimeEdit.setTime(QTime(1, 0, 0))
        self.startTimeEdit = QTimeEdit(Dialog)
        self.startTimeEdit.setObjectName(u"startTimeEdit")
        self.startTimeEdit.setEnabled(False)
        self.startTimeEdit.setGeometry(QRect(210, 280, 81, 32))
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 70, 271, 141))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.normalRadioButton = QRadioButton(self.groupBox)
        self.normalRadioButton.setObjectName(u"normalRadioButton")
        self.normalRadioButton.setChecked(True)

        self.verticalLayout.addWidget(self.normalRadioButton)

        self.peaksRadioButton = QRadioButton(self.groupBox)
        self.peaksRadioButton.setObjectName(u"peaksRadioButton")
        self.peaksRadioButton.setEnabled(False)

        self.verticalLayout.addWidget(self.peaksRadioButton)

        self.previewRadioButton = QRadioButton(self.groupBox)
        self.previewRadioButton.setObjectName(u"previewRadioButton")

        self.verticalLayout.addWidget(self.previewRadioButton)

        self.partialRadioButton = QRadioButton(self.groupBox)
        self.partialRadioButton.setObjectName(u"partialRadioButton")

        self.verticalLayout.addWidget(self.partialRadioButton)


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
        self.durationTimeEdit.setDisplayFormat(QCoreApplication.translate("Dialog", u"HH:mm", None))
        self.startTimeEdit.setDisplayFormat(QCoreApplication.translate("Dialog", u"HH:mm", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Import", None))
        self.normalRadioButton.setText(QCoreApplication.translate("Dialog", u"full import", None))
        self.peaksRadioButton.setText(QCoreApplication.translate("Dialog", u"full import with R peaks", None))
        self.previewRadioButton.setText(QCoreApplication.translate("Dialog", u"quick preview (one lead, downsampled)", None))
        self.partialRadioButton.setText(QCoreApplication.translate("Dialog", u"partial import", None))
    # retranslateUi

