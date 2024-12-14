import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
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

        self.ui.signalView.plotItem.setMouseEnabled(
            y=False)  # Only allow zoom in X-axis
        self.ui.signalView.showGrid(x=True, y=True)

        self._open_file("MRSY_06102022_1512.csv")

        self.ui.openPushButton.clicked.connect(self._open_file)
        self.ui.carpetView.view.sigRangeChanged.connect(self._panSignal)
        self.ui.cmapComboBox.currentIndexChanged.connect(self._update_cmap)
        self.ui.leadComboBox.currentIndexChanged.connect(self._update_lead)

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

        image, _ = utils.make_carpet(self.ecg[self.lead], self.rpeaks, first_r=0, beats=len(
            self.rpeaks), left_off=self.left_off, right_off=self.right_off)

        self.ui.carpetView.setImage(image.T)

    def _open_file(self, filename=False):
        if filename is False:
            self.filename, _ = QFileDialog.getOpenFileName(self, "Open ECG", "",
                                                       "ECG files (*.ecg *.hea *.csv);;Ishne ECG (*.ecg);;MIT ECG (*.hea);;CSV (*.csv)"
                                                       )
        else:
            self.filename = filename
        file_ext = self.filename[-3:]
        if file_ext == 'ecg':
            self.ecg, self.leads, self.sampling_rate, self.datetime = utils.load_ishne(
                self.filename)
        elif file_ext == 'hea':
            self.ecg, self.leads, self.sampling_rate, self.datetime = utils.load_mit(
                self.filename)
        elif file_ext == 'csv':
            self.ecg, self.leads, self.sampling_rate, self.datetime = utils.load_csv(
                self.filename)
        else:
            return
        
        self.ui.leadComboBox.clear()
        for lead in range(self.leads):
            self.ui.leadComboBox.addItem(f"Lead {lead+1}")

        self.lead=0
        self.left_off = self.sampling_rate
        self.right_off = 3*self.sampling_rate//2

        self.ecg = np.stack([nk.ecg_clean(sig, sampling_rate=self.sampling_rate) for sig in self.ecg])
        self.ecg /= self.ecg.std(axis=1, keepdims=True)

        _, self.rpeaks = nk.ecg_peaks(
            self.ecg[0], sampling_rate=self.sampling_rate, method='neurokit')
        self.rpeaks = self.rpeaks['ECG_R_Peaks']
        self.rpeaks = utils.cut_rpeaks(
            self.rpeaks, self.left_off, self.right_off, self.ecg.shape[-1])

   
        self._update_lead()

        view = self.ui.carpetView.getView()
        viewrange = self.left_off+self.right_off
        view.setLimits(xMin=0, xMax=viewrange, minXRange=viewrange, maxXRange=viewrange, minYRange=10, maxYRange=len(self.rpeaks), yMin=0, yMax=len(self.rpeaks))
        self.ui.carpetView.setLevels(-3, 3)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
