import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
import matplotlib.pyplot as plt  # Import matplotlib for colormap
import pyqtgraph as pg
from pyqtgraph import exporters
import numpy as np
import neurokit2 as nk
from pathlib import Path
import datetime

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

        # self.ui.signalView.plotItem.setMouseEnabled(y=False)  # Only allow zoom in X-axis
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
        self.ui.exportPushButton.clicked.connect(self._export_image)


    def _open_file(self, filename=False):
        if filename is False:
            self.filename, _ = QFileDialog.getOpenFileName(self, "Open ECG", "",
                                                       "ECG files (*.ecg *.hea *.csv *.ISHNE);;Ishne ECG (*.ecg *.ISHNE);;WFDB (MIT) ECG (*.hea)"
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
        
        self.ecg = record['signal']
        self.sampling_rate = record['sampling_rate']
        self.datetime = record['datetime']
        self.leads = record['n_sig']
        
        self.filenameLabel.setText(f'{"/".join(Path(self.filename).parts[-2:])}\t{self.sampling_rate} Hz\t{self.leads} leads')

        print(f"sampling rate: {self.sampling_rate}, leads: {self.leads}")
        
        self.lead=0
        self.rLead=0
        self.firstR = 0
        self.left_off = self.sampling_rate
        self.right_off = 3*self.sampling_rate//2
        self.ecg = utils.clean_ecg(self.ecg, self.sampling_rate)
        self.rpeaks = utils.get_rpeaks(self.ecg, self.sampling_rate, self.left_off, self.right_off, r_source_lead=0)

        # self.beats = min(self.default_beats, len(self.rpeaks))
        self.beats = len(self.rpeaks)

        self.ui.r1spinBox.setRange(0, len(self.rpeaks))
        self.ui.r1spinBox.setValue(0)
        self.ui.r2spinBox.setRange(8, len(self.rpeaks))
        self.ui.r2spinBox.setValue(self.beats)
        self.ui.r2spinBox.setSingleStep(max(1, len(self.rpeaks) // 50))  # Set single step to 1% of total R-peaks
   
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

        self.ui.signalView.setXRange(0, self.ecg.shape[1] / self.sampling_rate)

        self._update_lead()

        self.ui.carpetView.setXticks(self.left_off, self.right_off, self.sampling_rate)

    def _update_lead(self):
        self.lead = self.ui.leadComboBox.currentIndex()
        T = self.ecg.shape[1] / self.sampling_rate
        mn, mx = np.min(self.ecg[self.lead]), np.max(self.ecg[self.lead])
        p1, p2 = np.percentile(self.ecg[self.lead], [0.5, 99.5])

        t = np.arange(0, self.ecg.shape[1]) / self.sampling_rate
        self.ui.signalView.clear()
        self.ui.signalView.plot(t, self.ecg[self.lead])
        self.ui.signalView.plot(t[self.rpeaks], self.ecg[self.lead, self.rpeaks], pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(255, 0, 0, 128))
        self.ui.signalView.setYRange(p1, p2)
        self.ui.signalView.setLimits(xMin=0, xMax=T, yMin=1.1*mn, yMax=1.1*mx)

        image, _ = utils.make_carpet(self.ecg[self.lead], self.rpeaks, first_r=self.firstR, beats=self.beats, left_off=self.left_off, right_off=self.right_off)
        self.ui.carpetView.show(image)

        self.ui.carpetView.setLevels(p1, p2)
        hist = self.ui.carpetView.getHistogramWidget()
        hist.setHistogramRange(p1, p2)

    def _update_rpeaks(self):
        self.rLead = self.ui.rSourceLeadComboBox.currentIndex()
        self.rpeaks = utils.get_rpeaks(self.ecg, self.sampling_rate, self.left_off, self.right_off, r_source_lead=self.rLead)
        self.ui.r1spinBox.setMaximum(len(self.rpeaks))
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

    def RtoTime(self, R):
        if R < 0:
            return ""
        if R >= len(self.rpeaks):
            return ""
        R = int(R)
        totalSeconds = self.rpeaks[R]/self.sampling_rate
        return f"{datetime.timedelta(seconds=int(totalSeconds))}\n{R}RR"
    
    def _export_image(self):
        name = Path(self.filename).stem + '.png'
        filename, _ = QFileDialog.getSaveFileName(self, "Save Image", name, "PNG files (*.png);;JPEG files (*.jpg);;All files (*)")
        if filename:
            exporter = exporters.ImageExporter(self.ui.carpetView.view)
            exporter.export(filename)
            print(f"Image saved to {filename}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
