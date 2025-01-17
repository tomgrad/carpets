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

        self.ui.signalView.plotItem.setMouseEnabled(y=False)  # Only allow zoom in X-axis
        self.ui.signalView.showGrid(x=True, y=True)

        self.rpeaks = np.array([0])
        self.sampling_rate = 1
        self.firstR = 0
        self.default_beats = 500

        self.ui.openPushButton.clicked.connect(self._open_file)
        self.ui.cmapComboBox.currentIndexChanged.connect(self._update_cmap)
        self.ui.leadComboBox.currentIndexChanged.connect(self._update_lead)
        self.ui.updateRangePushButton.clicked.connect(self._update_range)
        self.ui.carpetView.view.sigRangeChanged.connect(self._panSignal)

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

        image, _ = utils.make_carpet(self.ecg[self.lead], self.rpeaks, first_r=self.firstR, beats=self.beats, left_off=self.left_off, right_off=self.right_off)

        view = self.ui.carpetView.getView()

        width = self.left_off+self.right_off
        sr = self.sampling_rate
        view.setAutoPan(y=True)
        # view.setAutoVisible(y=True)
        # view.setLimits(xMin=-100, xMax=viewrange, minXRange=viewrange, maxXRange=viewrange+200, minYRange=10, maxYRange=self.beats, yMin=0, yMax=len(self.rpeaks))
        self.ui.carpetView.setImage(image.T)
        view.setLimits(xMin=-sr//8, xMax=width+sr//8, 
                        minXRange=width+sr//4,
                        maxXRange=width+sr//4,
                        yMin=-2, yMax=self.beats+2,                       
                        minYRange=10, maxYRange=self.beats+4
                        )


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
        
        self.ecg = record['signal']
        self.sampling_rate = record['sampling_rate']
        self.datetime = record['datetime']
        self.leads = record['n_sig']

        self.beats = min(self.default_beats, self.ecg.shape[-1])
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

        self.ui.r1spinBox.setMaximum(len(self.rpeaks)-10)
        self.ui.r2spinBox.setMaximum(len(self.rpeaks))
        self.ui.r2spinBox.setMinimum(10)
        self.ui.r1spinBox.setValue(0)
        self.ui.r2spinBox.setValue(self.beats)
   
        self.ui.leadComboBox.blockSignals(True) # prevent _update_signal() from being triggered
        self.ui.leadComboBox.clear()
        for label in record['sig_name']:
            self.ui.leadComboBox.addItem(label)
        self.ui.leadComboBox.blockSignals(False)
        
        self._update_lead()

        self.ui.carpetView.setLevels(-3, 3)

        ax = self.ui.carpetView.getView().getAxis('bottom')
        ticks = np.linspace(0, self.left_off+self.right_off, 6)

        ax.setTicks([
           [(t.item(), str(int((t-self.sampling_rate)*1000/self.sampling_rate))) for t in ticks]
           ])
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
