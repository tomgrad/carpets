import os
from os.path import exists
from datetime import datetime, timedelta

import numpy as np
from ishneholterlib import Holter
import wfdb
import neurokit2 as nk


def load_ishne(filename):
    record = Holter(filename)
    record.load_data()
    dt = datetime(record.record_date.year, record.record_date.month,
                  record.record_date.day, record.start_time.hour, record.start_time.minute)
    # TODO: dodać sprawdzanie, czy odprowadzenie zawiera sygnał (np przez STD) - przypadek THEW
    return {'signal': np.stack([l.data for l in record.lead]),
            'n_sig': len(record.lead),
            'sampling_rate': record.sr,
            'datetime': dt,
            'record_name': filename,
            'sig_len': len(record.lead[0].data),
            'sig_name': [f'Lead {i+1}' for i in range(len(record.lead))]}


def load_csv(filename):
    record = np.loadtxt(filename, delimiter=',')
    if len(record.shape) == 1:
        record = record.reshape(1, -1)
    sr = 200  # zakodować w nazwie katalogu?
    dt = datetime(year=1980, month=5, day=2, hour=0, minute=0)
    return {'signal': record,
            'sampling_rate': sr,
            'datetime': dt,
            'n_sig': record.shape[0],
            'sig_len': record.shape[1],
            'sig_name': [f'Lead {i+1}' for i in range(record.shape[0])],
            'record_name': filename}


def load_wfdb(filename):
    base_fn = filename[:-4]
    record = wfdb.rdrecord(base_fn)
    try:
        dt = datetime(year=1980, month=5, day=2, hour=record.base_time.hour,
                      minute=record.base_time.minute, second=record.base_time.second)
    except:
        dt = datetime(year=1980, month=5, day=2, hour=0, minute=0)
    return {'signal': record.p_signal.T,
            'sampling_rate': record.fs,
            'record_name': record.record_name,
            'sig_len': record.sig_len,
            'datetime': dt,
            'n_sig': record.n_sig,
            'sig_name': record.sig_name}

def clean_ecg(ecg, sampling_rate):
    clean = np.stack([nk.ecg_clean(sig, sampling_rate=sampling_rate) for sig in ecg])
    clean /= clean.std(axis=1, keepdims=True)
    return clean

def get_rpeaks(ecg, sampling_rate, left_off, right_off, r_source_lead=0):
    _, rpeaks = nk.ecg_peaks(
        ecg[r_source_lead], sampling_rate=sampling_rate, method='neurokit')
    rpeaks = rpeaks['ECG_R_Peaks']
    rpeaks = cut_rpeaks(rpeaks, left_off, right_off, ecg.shape[-1])
    return rpeaks


def make_carpet(ecg, rpeaks, first_r, beats=512, left_off=256, right_off=256):
    rp = rpeaks[first_r:first_r+beats]
    result = [ecg[r-left_off:r+right_off] for r in rp]
    return np.stack(result), rp

def cut_rpeaks(rpeaks, left_off, right_off, length):
    first = next(i for i, x in enumerate(rpeaks) if x > left_off)
    last = len(rpeaks) - next(i for i, x in enumerate(rpeaks[::-1]) if x < length-right_off)
    return rpeaks[first:last]