import os
from os.path import exists
from datetime import datetime, timedelta

import numpy as np
from ishneholterlib import Holter
import wfdb
import neurokit2 as nk


def load_ishne(filename, lead=0):
    record = Holter(filename)
    print(record.__dict__)
    record.load_data()
    dt = datetime(record.record_date.year, record.record_date.month,
                  record.record_date.day, record.start_time.hour, record.start_time.minute)
    return np.stack([l.data for l in record.lead]), len(record.lead), record.sr, dt
    # return record.lead[lead].data, 1, record.sr, dt


def load_csv(filename):
    record = np.loadtxt(filename, delimiter=',')
    if len(record.shape) == 1:
        record = record.reshape(1, -1)
    sr = 200  # zakodować w nazwie katalogu?
    dt = datetime(year=1980, month=5, day=2, hour=0, minute=0)

    return record, record.shape[0], sr, dt


def load_mit(filename):
    base_fn = filename[:-4]
    record = wfdb.rdrecord(base_fn)
    # print(record.__dict__)
    try:
        dt = datetime(year=1980, month=5, day=2, hour=record.base_time.hour,
                      minute=record.base_time.minute, second=record.base_time.second)
    except:
        dt = datetime(year=1980, month=5, day=2, hour=0, minute=0)
    return record.p_signal.T, record.p_signal.shape[1], record.fs, dt


def make_carpet(ecg, rpeaks, first_r, beats=512, left_off=256, right_off=256):
    rp = rpeaks[first_r:first_r+beats]
    result = [ecg[r-left_off:r+right_off] for r in rp]
    return np.stack(result), rp

def cut_rpeaks(rpeaks, left_off, right_off, length):
    first = next(i for i, x in enumerate(rpeaks) if x > left_off)
    last = len(rpeaks) - next(i for i, x in enumerate(rpeaks[::-1]) if x < length-right_off)
    return rpeaks[first:last]