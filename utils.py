from datetime import datetime
from pathlib import Path

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
            'sig_name': [f'Lead {i+1}' for i in range(len(record.lead))],
            'rpeaks': None}


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
            'record_name': filename,
            'rpeaks': None}


def load_wfdb(filename, ann = False):
    base_fn = filename[:-4]
    record = wfdb.rdrecord(base_fn)

    if ann:
        # check if annotation file exists (with .qrs or .atr extension)
        if Path(base_fn + '.qrs').exists():
            ann = wfdb.rdann(base_fn, 'qrs')
        elif Path(base_fn + '.atr').exists():
            ann = wfdb.rdann(base_fn, 'atr')
        else:
            ann = None
    else:
        ann = None

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
            'sig_name': record.sig_name,
            'rpeaks': ann.sample if ann else None}


def load_amedtec_ecgpro(filename):
    record=dict()
    with open(filename, 'rb') as f:
        header = f.read(988)
        record['record_name'] = Path(filename).stem
        
        dt=header[384:403].decode('utf-8')
        record['datetime'] = datetime.strptime(dt, '%d.%m.%Y %H:%M:%S')
        record['sampling_rate'] = int(header[834:838].decode('utf-8'))
        LSBperMV = header[839:843].decode('utf-8')
        fileVersion = header[987]
        record['sig_len'] = int.from_bytes(f.read(4), 'little')
        record['n_sig'] = int.from_bytes(f.read(2), 'little')
        # channelCodes = [int(x) for x in np.frombuffer(f.read(15*2), dtype=np.int16)]
        record['sig_name'] = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']

        dt = np.int16 if fileVersion == 1 else np.int32
        word_size = 2 if fileVersion == 1 else 4

        ecg = np.frombuffer(f.read(record['n_sig']*record['sig_len']*word_size), dtype=dt)
        ecg = ecg.reshape(-1, record['n_sig']) / int(LSBperMV)
        record['signal'] = ecg.T
        record['rpeaks'] = None
    return record


def clean_ecg(ecg, sampling_rate):
    clean = np.stack([nk.ecg_clean(sig, sampling_rate=sampling_rate) for sig in ecg])
    clean /= clean.std(axis=1, keepdims=True)
    return clean

def detrend_ecg(ecg):
    detrended = np.stack([nk.signal.signal_detrend(sig) for sig in ecg])
    detrended /= detrended.std(axis=1, keepdims=True)
    return detrended

def filter_ecg(ecg, sampling_rate, lowcut=0.1, highcut=None):
    filtered = np.stack([nk.signal.signal_filter(sig, sampling_rate=sampling_rate,
                                                lowcut=lowcut, highcut=highcut, method='butterworth', order=5)
                         for sig in ecg])
    return filtered


def get_rpeaks(ecg, sampling_rate, left_off, right_off, r_source_lead=0):
    _, rpeaks = nk.ecg_peaks(
        ecg[r_source_lead], sampling_rate=sampling_rate, method='neurokit')
    rpeaks = rpeaks['ECG_R_Peaks']
    # rpeaks = cut_rpeaks(rpeaks, left_off, right_off, ecg.shape[-1])
    return rpeaks


def make_carpet(ecg, rpeaks, first_r, beats=512, left_off=256, right_off=256):
    if rpeaks[first_r] < left_off:
        first_r = next(i for i, r in enumerate(rpeaks) if r > left_off)
    beats = min(beats, len(rpeaks) - first_r)
    if rpeaks[first_r+beats-1] > len(ecg) - right_off:
        beats = next(i for i, r in enumerate(rpeaks[first_r:]) if r > len(ecg) - right_off)
    rp = rpeaks[first_r:first_r+beats]
    result = [ecg[r-left_off:r+right_off] for r in rp]
    return np.stack(result), rp

def cut_rpeaks(rpeaks, left_off, right_off, length):
    first = next(i for i, x in enumerate(rpeaks) if x > left_off)
    last = len(rpeaks) - next(i for i, x in enumerate(rpeaks[::-1]) if x < length-right_off)
    return rpeaks[first:last]