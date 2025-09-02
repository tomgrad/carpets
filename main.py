import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
import pyqtgraph as pg
from pyqtgraph import exporters
import numpy as np
from pathlib import Path
import datetime
import utils

from importer import ImportDialog
from ui_mainwindow import Ui_MainWindow

# pg.setConfigOption('background', 'k')
# pg.setConfigOption('foreground', 'w')
pg.setConfigOptions(antialias=True)

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.signalView.showGrid(x=True, y=True)
        self.signalView.plotItem.getViewBox().setAutoVisible(y=True)
        self.carpetView.RtoTime = self.RtoTime

        self.carpetView.setEnabled(False)
        self.signalView.setEnabled(False)

        self.rpeaks = [np.array([])]
        self.rLead = 0
        self.xUnit = 'ms'
        self.sampling_rate = 1
        self.statusLabel = QLabel("Open an ECG file to start")
        self.statusbar.addPermanentWidget(self.statusLabel)
        self.openPushButton.clicked.connect(self._open_file)
        self.cmapComboBox.currentIndexChanged.connect(self._update_cmap)
        self.themeComboBox.currentIndexChanged.connect(self._set_theme)
        self.fontSizeSpinBox.valueChanged.connect(lambda: self.carpetView.setFontSize(self.fontSizeSpinBox.value()))
        self.leadComboBox.currentIndexChanged.connect(self._update_lead)
        self.carpetView.view.sigRangeChanged.connect(self._panSignal)
        self.rSourceLeadComboBox.currentIndexChanged.connect(self._update_rpeaks)
        self.exportImagePushButton.clicked.connect(self._export_image)
        self.exportPeaksPushButton.clicked.connect(self._export_peaks)
        self.fixedHeightCheckBox.stateChanged.connect(self._set_limits)
        self.fixedHeightSpinBox.valueChanged.connect(lambda: self._set_limits(self.fixedHeightCheckBox.checkState().value))
        self.lineWidthSpinBox.valueChanged.connect(self.updateLineWidth)
        self.autolevelsPushButton.clicked.connect(self._autolevels)
        self.msRadioButton.toggled.connect(self._set_ms_unit)
        self.bpmRadioButton.toggled.connect(self._set_bpm_unit)

    def _open_file(self, filename=False):
        importer = ImportDialog()
        record = importer.run()

        if not record:
            return

        self.ecg = record['ecg']
        self.rpeaks = record['rpeaks']
        self.filename = record['filename']
        self.sampling_rate = record['sampling_rate']
        self.datetime = record['datetime']
        self.leads = record['leads']

        status = f'{"/".join(Path(self.filename).parts[-2:])}\t{self.sampling_rate} Hz\t{self.leads} leads'
        status += f"\tStart: {str(self.datetime).split()[-1]}"
        if record['start_time']:
            status += f'\toffset: +{record['start_time']} hours'
        self.statusLabel.setText(status)

        self.lead=0
        self.rLead=record['rlead']
        self.left_off = self.sampling_rate
        self.right_off = 3*self.sampling_rate//2

        if len(self.rpeaks[self.rLead]) == 0:   # if no R peaks are loaded
            self.rpeaks[self.rLead] = utils.get_rpeaks(self.ecg, self.sampling_rate, self.left_off, self.right_off, r_source_lead=self.rLead)
   
        self.leadComboBox.blockSignals(True) # prevent _update_signal() from being triggered
        self.rSourceLeadComboBox.blockSignals(True)
        self.leadComboBox.clear()
        self.rSourceLeadComboBox.clear()
        for label in record['sig_name']:
            self.leadComboBox.addItem(label)
            self.rSourceLeadComboBox.addItem(label)
        self.leadComboBox.blockSignals(False)
        self.rSourceLeadComboBox.setCurrentIndex(self.rLead)
        self.rSourceLeadComboBox.blockSignals(False)

        self.carpetView.setEnabled(True)
        self.signalView.setEnabled(True)
        self.fixedHeightCheckBox.setChecked(False)
        self.signalView.setXRange(0, self.ecg.shape[1] / self.sampling_rate)
        self._update_lead(self.lead, reset_range=True)
        self.carpetView.setXticks(self.left_off, self.right_off, self.sampling_rate, unit=self.xUnit)
        self.exportPeaksPushButton.setEnabled(record['allow_export_peaks'])
    
    def _update_lead(self, lead, reset_range=False):
        self.lead = lead
        rpeaks = self.rpeaks[self.rLead]
        T = self.ecg.shape[1] / self.sampling_rate
        mn, mx = np.min(self.ecg[self.lead]), np.max(self.ecg[self.lead])
        p1, p2 = np.percentile(self.ecg[self.lead], [0.5, 99.5])

        t = np.arange(0, self.ecg.shape[1]) / self.sampling_rate
        self.signalView.clear()
        self.signalView.plot(t, self.ecg[self.lead], pen=pg.mkPen(width=self.lineWidthSpinBox.value()))
        self.signalView.plot(t[rpeaks], self.ecg[self.lead, rpeaks], pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(255, 0, 0, 128))
        self.signalView.setYRange(p1, p2)
        self.signalView.setLimits(xMin=0, xMax=T, yMin=1.1*mn, yMax=1.1*mx)

        image, _ = utils.make_carpet(self.ecg[self.lead], rpeaks, first_r=0, beats=len(rpeaks), left_off=self.left_off, right_off=self.right_off)
        self.carpetView.setImage(image.T, autoRange=False)
        if reset_range==True:
            self.carpetView.resetRange()

        self.carpetView.setLevels(p1, p2)
        hist = self.carpetView.getHistogramWidget()
        hist.setHistogramRange(p1, p2)

    def _update_rpeaks(self):
        self.rLead = self.rSourceLeadComboBox.currentIndex()
        if len(self.rpeaks[self.rLead]) == 0:
            self.rpeaks[self.rLead] = utils.get_rpeaks(self.ecg, self.sampling_rate, self.left_off, self.right_off, r_source_lead=self.rLead)
        self._update_lead(self.lead, reset_range=False)
        self.carpetView.resetLimits() # update the number of rows/segments
      
    def _set_limits(self, state):
        if state == 2:
            height = self.fixedHeightSpinBox.value()
            self.carpetView.view.setLimits(minYRange=height, maxYRange=height)
        else:
            _, height = self.carpetView.getImageItem().image.shape
            self.carpetView.view.setLimits(minYRange=5, maxYRange=1.05*height)

    def _panSignal(self):
        rpeaks = self.rpeaks[self.rLead]
        r_range = self.carpetView.view.viewRange()[1]
        r1, r2 = int(r_range[0]), int(r_range[1])
        r1 = max(0, r1)
        r2 = min(rpeaks.shape[0]-1, r2)
        self.signalView.setXRange(
            rpeaks[r1]/self.sampling_rate, rpeaks[r2]/self.sampling_rate)

    def _update_cmap(self):
        cmap = self.cmapComboBox.currentText()
        cm = pg.colormap.getFromMatplotlib(cmap)
        self.carpetView.setColorMap(cm)

    def _autolevels(self):
        p = self.autolevelsSpinBox.value()
        p1, p2 = np.percentile(self.ecg[self.lead], [p, 100-p])
        self.carpetView.setLevels(p1, p2)

    def RtoTime(self, R):
        if R < 0:
            return ""
        if R >= len(self.rpeaks[self.rLead]):
            return ""
        R = int(R)
        totalSeconds = self.rpeaks[self.rLead][R]/self.sampling_rate
        return f"{datetime.timedelta(seconds=int(totalSeconds))}\n{R}RR"
    

    def _set_ms_unit(self):
        self.xUnit = 'ms'
        self.carpetView.setXticks(self.left_off, self.right_off, self.sampling_rate, unit='ms')

    def _set_bpm_unit(self):
        self.xUnit = 'bpm'
        self.carpetView.setXticks(self.left_off, self.right_off, self.sampling_rate, unit='bpm')
    
    def _set_theme(self):
        theme = self.themeComboBox.currentText()
        if theme == 'dark':
            self.carpetView.getView().getViewWidget().setBackground('k')
            self.carpetView.getView().getAxis('left').setTextPen(pg.mkPen('#969696'))
            self.carpetView.getView().getAxis('bottom').setTextPen(pg.mkPen('#969696'))
        elif theme == 'light':
            self.carpetView.getView().getViewWidget().setBackground('w')
            self.carpetView.getView().getAxis('left').setTextPen(pg.mkPen('k'))
            self.carpetView.getView().getAxis('bottom').setTextPen(pg.mkPen('k'))

    def _export_image(self):
        name = Path(self.filename).stem + '.png'
        filename, _ = QFileDialog.getSaveFileName(self, "Save Image", name, "PNG files (*.png);;JPEG files (*.jpg);;All files (*)")
        if filename:
            exporter = exporters.ImageExporter(self.carpetView.view)
            exporter.parameters()['height'] = 1080
            exporter.export(filename)
            print(f"Image saved to {filename}")

    def _export_peaks(self):
        name = str(Path(self.filename).with_suffix('.rpeaks'))
        filename, _ = QFileDialog.getSaveFileName(self, "Save R peaks", name, "R peaks files (*.rpeaks);;All files (*)")
        if filename:
            print(f"Exporting R peaks to {filename}")
            for i, rpeaks in enumerate(self.rpeaks):
                if len(rpeaks) == 0:
                    self.rpeaks[i] = utils.get_rpeaks(self.ecg, self.sampling_rate, self.left_off, self.right_off, r_source_lead=i)
            with open(filename, 'w') as f:
                for i, rpeaks in enumerate(self.rpeaks):
                    f.write(f"\t".join(map(str, rpeaks)) + "\n")
            print(f"Done.")

    def updateLineWidth(self, value):
        plot = self.signalView.plotItem.items[0]  
        pen = plot.opts['pen']
        pen.setWidth(value)
        plot.setPen(pen)
       
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
