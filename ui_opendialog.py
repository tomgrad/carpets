# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'opendialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QDoubleSpinBox, QFormLayout, QGroupBox, QLabel,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(350, 380)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(170, 340, 171, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.durationLabel = QLabel(Dialog)
        self.durationLabel.setObjectName(u"durationLabel")
        self.durationLabel.setGeometry(QRect(10, 10, 301, 17))
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 30, 331, 111))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.normalRadioButton = QRadioButton(self.groupBox)
        self.normalRadioButton.setObjectName(u"normalRadioButton")
        self.normalRadioButton.setChecked(True)

        self.verticalLayout.addWidget(self.normalRadioButton)

        self.previewRadioButton = QRadioButton(self.groupBox)
        self.previewRadioButton.setObjectName(u"previewRadioButton")

        self.verticalLayout.addWidget(self.previewRadioButton)

        self.partialRadioButton = QRadioButton(self.groupBox)
        self.partialRadioButton.setObjectName(u"partialRadioButton")

        self.verticalLayout.addWidget(self.partialRadioButton)

        self.formLayoutWidget_2 = QWidget(Dialog)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(150, 150, 190, 171))
        self.formLayout_3 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.durationSpinBox = QSpinBox(self.formLayoutWidget_2)
        self.durationSpinBox.setObjectName(u"durationSpinBox")
        self.durationSpinBox.setEnabled(False)
        self.durationSpinBox.setMinimum(1)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.durationSpinBox)

        self.label_3 = QLabel(self.formLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.startSpinBox = QSpinBox(self.formLayoutWidget_2)
        self.startSpinBox.setObjectName(u"startSpinBox")
        self.startSpinBox.setEnabled(False)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.startSpinBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout_3.setItem(2, QFormLayout.ItemRole.FieldRole, self.verticalSpacer)

        self.label_2 = QLabel(self.formLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.lowcutSpinBox = QDoubleSpinBox(self.formLayoutWidget_2)
        self.lowcutSpinBox.setObjectName(u"lowcutSpinBox")
        self.lowcutSpinBox.setDecimals(1)
        self.lowcutSpinBox.setSingleStep(0.100000000000000)
        self.lowcutSpinBox.setValue(0.100000000000000)

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lowcutSpinBox)

        self.label_4 = QLabel(self.formLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.highcutSpinBox = QDoubleSpinBox(self.formLayoutWidget_2)
        self.highcutSpinBox.setObjectName(u"highcutSpinBox")
        self.highcutSpinBox.setDecimals(1)
        self.highcutSpinBox.setMaximum(250.000000000000000)
        self.highcutSpinBox.setSingleStep(10.000000000000000)
        self.highcutSpinBox.setValue(50.000000000000000)

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.FieldRole, self.highcutSpinBox)

        self.label = QLabel(self.formLayoutWidget_2)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 150, 131, 171))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cleanRadioButton = QRadioButton(self.groupBox_2)
        self.cleanRadioButton.setObjectName(u"cleanRadioButton")
        self.cleanRadioButton.setChecked(True)

        self.verticalLayout_2.addWidget(self.cleanRadioButton)

        self.detrendRadioButton = QRadioButton(self.groupBox_2)
        self.detrendRadioButton.setObjectName(u"detrendRadioButton")

        self.verticalLayout_2.addWidget(self.detrendRadioButton)

        self.filterRadioButton = QRadioButton(self.groupBox_2)
        self.filterRadioButton.setObjectName(u"filterRadioButton")

        self.verticalLayout_2.addWidget(self.filterRadioButton)

        self.hpfRadioButton = QRadioButton(self.groupBox_2)
        self.hpfRadioButton.setObjectName(u"hpfRadioButton")

        self.verticalLayout_2.addWidget(self.hpfRadioButton)

        self.lpfRadioButton = QRadioButton(self.groupBox_2)
        self.lpfRadioButton.setObjectName(u"lpfRadioButton")

        self.verticalLayout_2.addWidget(self.lpfRadioButton)

        self.rawRadioButton = QRadioButton(self.groupBox_2)
        self.rawRadioButton.setObjectName(u"rawRadioButton")

        self.verticalLayout_2.addWidget(self.rawRadioButton)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Import", None))
        self.durationLabel.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Import", None))
        self.normalRadioButton.setText(QCoreApplication.translate("Dialog", u"full import", None))
        self.previewRadioButton.setText(QCoreApplication.translate("Dialog", u"quick preview (one lead, downsampled)", None))
        self.partialRadioButton.setText(QCoreApplication.translate("Dialog", u"partial import", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"starting from (HH)", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"lower cutoff", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"upper cutoff", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Import only (HH)", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"preprocess", None))
        self.cleanRadioButton.setText(QCoreApplication.translate("Dialog", u"ecg_clean", None))
        self.detrendRadioButton.setText(QCoreApplication.translate("Dialog", u"signal_detrend", None))
        self.filterRadioButton.setText(QCoreApplication.translate("Dialog", u"band-pass", None))
        self.hpfRadioButton.setText(QCoreApplication.translate("Dialog", u"high-pass", None))
        self.lpfRadioButton.setText(QCoreApplication.translate("Dialog", u"low-pass", None))
        self.rawRadioButton.setText(QCoreApplication.translate("Dialog", u"none", None))
    # retranslateUi

