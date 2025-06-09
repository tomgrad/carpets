import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QDialog
import pyqtgraph as pg
from pyqtgraph import exporters
import numpy as np
from pathlib import Path
import datetime
import utils

from ui_mainwindow import Ui_MainWindow
from ui_opendialog import Ui_Dialog

# pg.setConfigOption('background', 'k')
# pg.setConfigOption('foreground', 'w')

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.signalView.showGrid(x=True, y=True)
        self.ui.signalView.plotItem.getViewBox().setAutoVisible(y=True)
        self.ui.carpetView.RtoTime = self.RtoTime

        self.rpeaks = [np.array([])]
        self.rLead = 0
        self.sampling_rate = 1
        self.statusLabel = QLabel("Open an ECG file to start")
        self.ui.statusbar.addPermanentWidget(self.statusLabel)
        self.ui.openPushButton.clicked.connect(self._open_file)

    def connect_signals(self):
        self.ui.cmapComboBox.currentIndexChanged.connect(self._update_cmap)
        self.ui.leadComboBox.currentIndexChanged.connect(self._update_lead)
        self.ui.carpetView.view.sigRangeChanged.connect(self._panSignal)
        self.ui.rSourceLeadComboBox.currentIndexChanged.connect(self._update_rpeaks)
        self.ui.exportImagePushButton.clicked.connect(self._export_image)
        self.ui.exportPeaksPushButton.clicked.connect(self._export_peaks)
        self.ui.themeComboBox.currentIndexChanged.connect(self._set_theme)
        self.ui.fixedHeightCheckBox.stateChanged.connect(self._set_limits)
        self.ui.fixedHeightSpinBox.valueChanged.connect(lambda: self._set_limits(self.ui.fixedHeightCheckBox.checkState().value))

    def _open_file(self, filename=False):
        if filename is False:
            self.filename, _ = QFileDialog.getOpenFileName(self, "Open ECG", "",
                                                       "ECG files (*.ecg *.hea *.dat *.ISHNE);;Ishne ECG (*.ecg *.ISHNE);;WFDB (MIT) ECG (*.hea);;AMEDTEC ECGPro (*.dat)"
                                                       )
        else:
            self.filename = filename
        file_ext = self.filename.split('.')[-1]
        if file_ext == 'ecg' or file_ext == 'ISHNE':
            record = utils.load_ishne(self.filename)
        elif file_ext == 'hea':
            record = utils.load_wfdb(self.filename)
        elif file_ext == 'dat':
            record = utils.load_amedtec_ecgpro(self.filename)
        elif file_ext == 'csv':
            record = utils.load_csv(self.filename)
        else:
            return

        self.sampling_rate = record['sampling_rate']
        self.datetime = record['datetime']
        self.leads = record['n_sig']
        
        duration = record['sig_len'] // record['sampling_rate']

        ss = None # start time

        if duration > 60 * 60:  # more than 1 hour show dialog
            ui = Ui_Dialog()
            dialog = QDialog(self)
            ui.setupUi(dialog)
            ui.durationLabel.setText(f"Duration: {datetime.timedelta(seconds=duration)}")
            ui.startTimeEdit.setTimeRange(
                datetime.time(0), datetime.time(min(23, duration // 3600), 59, 59))

            if dialog.exec() == QDialog.Accepted:
                if ui.preview.isChecked():
                    self.sampling_rate //= 2
                    self.ecg = record['signal'][:1, ::2]
                else:
                    ss=ui.startTimeEdit.time()
                    tt=ui.durationTimeEdit.time()
                    startSamples = (ss.hour() * 3600 + ss.minute() * 60 + ss.second()) * self.sampling_rate
                    durationSamples = (tt.hour() * 3600 + tt.minute() * 60 + tt.second()) * self.sampling_rate
                    self.ecg = record['signal'][:, startSamples:startSamples + durationSamples]
            else:
                self.ecg = record['signal']
        else:
            self.ecg = record['signal']
       
        status = f'{"/".join(Path(self.filename).parts[-2:])}\t{self.sampling_rate} Hz\t{self.leads} leads'
        status += f"\tStart: {str(self.datetime).split()[-1]}"
        if ss is not None:
            status += f'\toffset: +{ss.toString("hh:mm:ss")}'
        self.statusLabel.setText(status)
        
        self.rpeaks = [[]]*self.leads

        self.lead=0
        self.rLead=0
        self.left_off = self.sampling_rate
        self.right_off = 3*self.sampling_rate//2
        self.ecg = utils.clean_ecg(self.ecg, self.sampling_rate)
        self.rpeaks[0] = utils.get_rpeaks(self.ecg, self.sampling_rate, self.left_off, self.right_off, r_source_lead=0)
        self.beats = len(self.rpeaks[0])
   
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

        self.connect_signals()

        self.ui.signalView.setXRange(0, self.ecg.shape[1] / self.sampling_rate)

        self._update_lead(self.lead, reset_range=True)

        self.ui.carpetView.setXticks(self.left_off, self.right_off, self.sampling_rate)
    

    def _update_lead(self, lead, reset_range=False):
        self.lead = lead
        rpeaks = self.rpeaks[self.rLead]
        T = self.ecg.shape[1] / self.sampling_rate
        mn, mx = np.min(self.ecg[self.lead]), np.max(self.ecg[self.lead])
        p1, p2 = np.percentile(self.ecg[self.lead], [0.5, 99.5])

        t = np.arange(0, self.ecg.shape[1]) / self.sampling_rate
        self.ui.signalView.clear()
        self.ui.signalView.plot(t, self.ecg[self.lead])
        self.ui.signalView.plot(t[rpeaks], self.ecg[self.lead, rpeaks], pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(255, 0, 0, 128))
        self.ui.signalView.setYRange(p1, p2)
        self.ui.signalView.setLimits(xMin=0, xMax=T, yMin=1.1*mn, yMax=1.1*mx)

        image, _ = utils.make_carpet(self.ecg[self.lead], rpeaks, first_r=0, beats=len(rpeaks), left_off=self.left_off, right_off=self.right_off)
        self.ui.carpetView.setImage(image.T, autoRange=False)
        if reset_range==True:
            self.ui.carpetView.resetRange()

        self.ui.carpetView.setLevels(p1, p2)
        hist = self.ui.carpetView.getHistogramWidget()
        hist.setHistogramRange(p1, p2)

    def _update_rpeaks(self):
        self.rLead = self.ui.rSourceLeadComboBox.currentIndex()
        if len(self.rpeaks[self.rLead]) == 0:
            self.rpeaks[self.rLead] = utils.get_rpeaks(self.ecg, self.sampling_rate, self.left_off, self.right_off, r_source_lead=self.rLead)
        self._update_lead(self.lead)
      
    def _set_limits(self, state):
        if state == 2:
            height = self.ui.fixedHeightSpinBox.value()
            self.ui.carpetView.view.setLimits(minYRange=height, maxYRange=height)
        else:
            _, height = self.ui.carpetView.getImageItem().image.shape
            self.ui.carpetView.view.setLimits(minYRange=5, maxYRange=1.05*height)

    def _panSignal(self):
        rpeaks = self.rpeaks[self.rLead]
        r_range = self.ui.carpetView.view.viewRange()[1]
        r1, r2 = int(r_range[0]), int(r_range[1])
        r1 = max(0, r1)
        r2 = min(rpeaks.shape[0]-1, r2)
        self.ui.signalView.setXRange(
            rpeaks[r1]/self.sampling_rate, rpeaks[r2]/self.sampling_rate)

    def _update_cmap(self):
        cmap = self.ui.cmapComboBox.currentText()
        cm = pg.colormap.getFromMatplotlib(cmap)
        self.ui.carpetView.setColorMap(cm)

    def RtoTime(self, R):
        if R < 0:
            return ""
        if R >= len(self.rpeaks[self.rLead]):
            return ""
        R = int(R)
        totalSeconds = self.rpeaks[self.rLead][R]/self.sampling_rate
        return f"{datetime.timedelta(seconds=int(totalSeconds))}\n{R}RR"
    
    def _set_theme(self):
        theme = self.ui.themeComboBox.currentText()
        if theme == 'dark':
            self.ui.carpetView.getView().getViewWidget().setBackground('k')
            self.ui.carpetView.getView().getAxis('left').setTextPen(pg.mkPen('w'))
            self.ui.carpetView.getView().getAxis('bottom').setTextPen(pg.mkPen('w'))
          
        elif theme == 'light':
            self.ui.carpetView.getView().getViewWidget().setBackground('w')
            self.ui.carpetView.getView().getAxis('left').setTextPen(pg.mkPen('k'))
            self.ui.carpetView.getView().getAxis('bottom').setTextPen(pg.mkPen('k'))

        else:
            print(f"Unknown theme: {theme}")
            return

    def _export_image(self):
        name = Path(self.filename).stem + '.png'
        filename, _ = QFileDialog.getSaveFileName(self, "Save Image", name, "PNG files (*.png);;JPEG files (*.jpg);;All files (*)")
        if filename:
            exporter = exporters.ImageExporter(self.ui.carpetView.view)
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
       
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
