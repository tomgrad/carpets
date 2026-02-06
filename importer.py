import sys
from pathlib import Path
import datetime
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog
from ui_opendialog import Ui_Dialog
import utils
import numpy as np


class ImportDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        fn, _ = QFileDialog.getOpenFileName(self, "Open ECG", "",
                                                       "WFDB (MIT) ECG (*.hea);;Ishne ECG (*.ecg *.ISHNE);;AMEDTEC ECGPro (*.dat);;ECG files (*.ecg *.hea *.dat *.ISHNE)"
                                                       )
        if fn:
            self.filename = fn
            self._open(fn)
        else:
            self.filename = None

    def _open(self, filename):
        file_ext = filename.split('.')[-1]
        if file_ext == 'ecg' or file_ext == 'ISHNE':
            self.record = utils.load_ishne(filename)
        elif file_ext == 'hea':
            self.record = utils.load_wfdb(filename, ann=True)
        elif file_ext == 'dat':
            self.record = utils.load_amedtec_ecgpro(filename)
        elif file_ext == 'csv':
            self.record = utils.load_csv(filename)
        else:
            return

        self.sampling_rate = self.record['sampling_rate']
        self.datetime = self.record['datetime']
        self.leads = self.record['n_sig']
        duration = self.record['sig_len'] // self.record['sampling_rate']
        self.sig_name = self.record['sig_name']
        self.ann = self.record['rpeaks']
       
        self.durationLabel.setText(f"Duration: {datetime.timedelta(seconds=duration)}  SR: {self.sampling_rate} Hz  Leads: {self.leads}")
        self.startSpinBox.setRange(0, duration // 3600)
        self.durationSpinBox.setRange(0, max(1, duration // 3600))
        # self.rLeadSpinBox.setRange(0, self.leads - 1)

        self.partialRadioButton.toggled.connect(lambda state: self.startSpinBox.setEnabled(state))
        self.partialRadioButton.toggled.connect(lambda state: self.durationSpinBox.setEnabled(state))

        # check if .rpeaks file exists
        # Check if any of multiple files with different suffixes exist
        # suffixes = ['.ann', '.qrs', '.xyz']
        # self.extra_files = [Path(self.filename).with_suffix(s) for s in suffixes]
        # self.any_extra_file_exists = any(f.exists() for f in self.extra_files)
        # if self.rpeaks_file.exists():
        #     self.peaksRadioButton.setEnabled(True)

    def run(self):
        if self.filename and self.exec() == QDialog.Accepted:
            result = {}
            result['filename'] = self.filename
            # result['allow_export_peaks'] = True
            rpeaks = [[]]*self.leads

            if self.previewRadioButton.isChecked():
                self.sampling_rate //= 2
                ecg = self.record['signal'][:1, ::2]
                self.record['sig_name'] = self.record['sig_name'][:1]
                # result['allow_export_peaks'] = False
            elif self.partialRadioButton.isChecked():
                ss=self.startSpinBox.value() * 3600 * self.sampling_rate
                tt=self.durationSpinBox.value() * 3600 * self.sampling_rate
                ecg = self.record['signal'][:, ss:ss + tt]
                # result['allow_export_peaks'] = False
            # elif self.peaksRadioButton.isChecked():
            #     ecg = self.record['signal']
            #     with open(self.rpeaks_file, 'r') as f:
            #         lines = f.readlines()
            #     rpeaks = [np.array(list(map(int, line.strip().split()))) for line in lines]
            else:
                ecg = self.record['signal']

            if self.cleanRadioButton.isChecked():
                ecg = utils.clean_ecg(ecg, self.sampling_rate)
            elif self.detrendRadioButton.isChecked():
                ecg = utils.detrend_ecg(ecg)
            elif self.filterRadioButton.isChecked():
                ecg = utils.filter_ecg(ecg, self.sampling_rate, lowcut=self.lowcutSpinBox.value(), highcut=self.highcutSpinBox.value())
            elif self.hpfRadioButton.isChecked():
                ecg = utils.filter_ecg(ecg, self.sampling_rate, lowcut=self.lowcutSpinBox.value(), highcut=None)
            elif self.lpfRadioButton.isChecked():
                ecg = utils.filter_ecg(ecg, self.sampling_rate, lowcut=None, highcut=self.highcutSpinBox.value())
            
            result['ecg'] = ecg
            result['sampling_rate'] = self.sampling_rate
            result['datetime'] = self.datetime
            result['leads'] = self.leads
            result['sig_name'] = self.sig_name
            result['rpeaks'] = rpeaks
            result['start_time'] = self.startSpinBox.value()
            # result['rlead'] = self.rLeadSpinBox.value()
            result['ann'] = self.ann
            return result
        else:
            return None


if __name__ == '__main__':

    app = QApplication(sys.argv)

    dialog = ImportDialog()
    dialog.run()
