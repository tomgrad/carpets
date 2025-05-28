import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
import matplotlib.pyplot as plt  # Import matplotlib for colormap
import pyqtgraph as pg
import numpy as np
import neurokit2 as nk

import utils

from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        statusbar = self.ui.statusbar
        self.filenameLabel = QLabel()
        statusbar.addWidget(self.filenameLabel)

        self.ui.signalView.plotItem.setMouseEnabled(y=False)  # Only allow zoom in X-axis
        self.ui.signalView.showGrid(x=True, y=True)
        self.ui.signalView.plotItem.getViewBox().setAutoVisible(y=True)
        self.ui.carpetView.RtoTime = self.RtoTime

        self.rpeaks = np.array([0])
        self.sampling_rate = 1
        self.firstR = 0
        self.default_beats = 500

        self.ui.openPushButton.clicked.connect(self._open_file)
        self.ui.cmapComboBox.currentIndexChanged.connect(self._update_cmap)
        self.ui.leadComboBox.currentIndexChanged.connect(self._update_lead)
        self.ui.updateRangePushButton.clicked.connect(self._update_range)
        self.ui.carpetView.view.sigRangeChanged.connect(self._panSignal)
        self.ui.rSourceLeadComboBox.currentIndexChanged.connect(self._update_rpeaks)

    def _update_rpeaks(self):
        self.rLead = self.ui.rSourceLeadComboBox.currentIndex()
        self.rpeaks = utils.get_rpeaks(self.ecg, self.sampling_rate, self.left_off, self.right_off, r_source_lead=self.rLead)
        self.ui.r1spinBox.setMaximum(len(self.rpeaks)-10)
        self.ui.r2spinBox.setMaximum(len(self.rpeaks))
        self.ui.r1spinBox.setValue(0)
        self.ui.r2spinBox.setValue(self.beats)
        self._update_lead()

    def _update_range(self):
        self.firstR = self.ui.r1spinBox.value()
        self.beats = self.ui.r2spinBox.value()
        self._update_lead()
       
    def _panSignal(self):
        r_range = self.ui.carpetView.view.viewRange()[1]
        r1, r2 = int(r_range[0]), int(r_range[1])
        r1 = max(0, r1)
        r2 = min(self.rpeaks.shape[0]-1, r2)
        self.ui.signalView.setXRange(
            self.rpeaks[r1]/self.sampling_rate, self.rpeaks[r2]/self.sampling_rate)

    def _update_cmap(self):
        cmap = self.ui.cmapComboBox.currentText()
        cm = pg.colormap.getFromMatplotlib(cmap)
        self.ui.carpetView.setColorMap(cm)

    def _update_lead(self):
        self.lead = self.ui.leadComboBox.currentIndex()
        t = np.arange(0, self.ecg.shape[1]) / self.sampling_rate
        self.ui.signalView.clear()
        self.ui.signalView.plot(t, self.ecg[self.lead])
        self.ui.signalView.plot(t[self.rpeaks], self.ecg[self.lead, self.rpeaks], pen=None, symbol='o', symbolPen=None, symbolSize=6, symbolBrush=(255, 255, 0, 128))


        image, _ = utils.make_carpet(self.ecg[self.lead], self.rpeaks, first_r=self.firstR, beats=self.beats, left_off=self.left_off, right_off=self.right_off)
        width = self.left_off+self.right_off
        sr = self.sampling_rate

        self.ui.carpetView.show(image)
        p1, p2 = np.percentile(self.ecg[self.lead], [0.5, 99.5])
        self.ui.carpetView.setLevels(p1, p2)
        hist = self.ui.carpetView.getHistogramWidget()
        hist.setHistogramRange(p1, p2)
        self.ui.signalView.setYRange(p1, p2)

    def _open_file(self, filename=False):
        if filename is False:
            self.filename, _ = QFileDialog.getOpenFileName(self, "Open ECG", "",
                                                       "ECG files (*.ecg *.hea *.csv *.ISHNE);;Ishne ECG (*.ecg *.ISHNE);;WFDB (MIT) ECG (*.hea);;CSV (*.csv)"
                                                       )
        else:
            self.filename = filename
        file_ext = self.filename.split('.')[-1]
        if file_ext == 'ecg' or file_ext == 'ISHNE':
            record = utils.load_ishne(self.filename)
        elif file_ext == 'hea':
            record = utils.load_wfdb(self.filename)
        elif file_ext == 'csv':
            record = utils.load_csv(self.filename)
        else:
            return
        
        self.filenameLabel.setText(self.filename)
        self.ecg = record['signal']
        self.sampling_rate = record['sampling_rate']
        self.datetime = record['datetime']
        self.leads = record['n_sig']

        print(f"sampling rate: {self.sampling_rate}, leads: {self.leads}")
        
        self.lead=0
        self.rLead=0
        self.left_off = self.sampling_rate
        self.right_off = 3*self.sampling_rate//2
        self.ecg = utils.clean_ecg(self.ecg, self.sampling_rate)
        self.rpeaks = utils.get_rpeaks(self.ecg, self.sampling_rate, self.left_off, self.right_off, r_source_lead=0)

        self.beats = min(self.default_beats, len(self.rpeaks))
        self.ui.r1spinBox.setMaximum(len(self.rpeaks)-10)
        self.ui.r2spinBox.setMaximum(len(self.rpeaks))
        self.ui.r1spinBox.setMinimum(0)
        self.ui.r2spinBox.setMinimum(10)
        self.ui.r1spinBox.setValue(0)
        self.ui.r2spinBox.setValue(self.beats)
   
        self.ui.leadComboBox.blockSignals(True) # prevent _update_signal() from being triggered
        self.ui.leadComboBox.clear()
        for label in record['sig_name']:
            self.ui.leadComboBox.addItem(label)
        self.ui.leadComboBox.blockSignals(False)

        self.ui.rSourceLeadComboBox.blockSignals(True) # prevent _update_signal() from being triggered
        self.ui.rSourceLeadComboBox.clear()
        for label in record['sig_name']:
            self.ui.rSourceLeadComboBox.addItem(label)
        self.ui.rSourceLeadComboBox.blockSignals(False)

        self._update_lead()

        self.ui.carpetView.setXticks(self.left_off, self.right_off, self.sampling_rate)

    def RtoTime(self, R):
        if R < 0:
            return ""
        if R >= len(self.rpeaks):
            return ""
        R = int(R)
        totalSeconds = self.rpeaks[R]/self.sampling_rate
        minutes = int(totalSeconds//60)
        seconds = int(totalSeconds%60)
        return f"{minutes:02d}:{seconds:02d}\n{R}RR"
    
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
