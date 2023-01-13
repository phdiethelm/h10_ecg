#!/usr/bin/python3

import argparse
from datetime import datetime
from datetime import date
import os

import numpy as np
import matplotlib.pyplot as plt

from dataclasses import dataclass

from scipy.signal import butter, sosfilt, sosfreqz
from skimage.restoration import (denoise_wavelet, estimate_sigma)

parser = argparse.ArgumentParser(description='Analyze Polar H10 ECG data')
parser.add_argument('filename', nargs='?', default="hr_data.bin")
args = parser.parse_args()

signature = 'H10 ECG v1.0 binary data'.encode('utf8')

with open(args.filename, mode="rb") as f:
    if f.read(len(signature)) != signature:
        print(f"Unknown file format!")
        os._exit(-1)
    
    @dataclass
    class xt_data():
        time: None
        value: None

    sampleRate = 130
    deltaT_ns = 1e9 / sampleRate

    ecg_data = xt_data(time=[], value=[])
    hr_data = xt_data(time=[], value=[])

    timestamp_ref = None

    while True:
        data_len = int.from_bytes(f.read(4), byteorder='little')
        data = f.read(data_len)

        if len(data) != data_len or data_len == 0:
            break
        
        if data[0] == 0x00: # 0x00 = ECG
            timestamp = int.from_bytes(data[1:][0:7], byteorder='little', signed=False)
            if timestamp_ref == None:
                timestamp_ref = datetime.fromtimestamp(timestamp/1e9)
            runtime = datetime.fromtimestamp(timestamp/1e9) - timestamp_ref
            print(f"Run time: {runtime}")
            i = 9
            sample = 0
            deltaT = 1e9/130.0
            
            frame_type = data[i]
            if frame_type == 0: # 0 = ECG Data
                i += 1
                d = []
                while len(data[i:][0:3]) == 3:
                    d.append(int.from_bytes(data[i:][0:2], byteorder='little', signed=True))
                    ecg_data.time.append(timestamp + sample * deltaT)
                    ecg_data.value.append(int.from_bytes(data[i:][0:2], byteorder='little', signed=True))
                    i += 3
                    sample += 1

    fig, ax1 = plt.subplots()
    ax1.plot(ecg_data.time, ecg_data.value)

    data = np.array(ecg_data.value)

    def thresholding_algo(y, lag, threshold, influence):
        signals = np.zeros(len(y))
        filteredY = np.array(y)
        avgFilter = [0]*len(y)
        stdFilter = [0]*len(y)
        avgFilter[lag - 1] = np.mean(y[0:lag])
        stdFilter[lag - 1] = np.std(y[0:lag])
        for i in range(lag, len(y)):
            if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
                if y[i] > avgFilter[i-1]:
                    signals[i] = 1
                else:
                    signals[i] = -1

                filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
                avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
                stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])
            else:
                signals[i] = 0
                filteredY[i] = y[i]
                avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
                stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])

        return np.asarray(signals)
        #return dict(signals = np.asarray(signals),
        #            avgFilter = np.asarray(avgFilter),
        #            stdFilter = np.asarray(stdFilter))

    ax2 = ax1.twinx()
    ax2.plot(ecg_data.time, thresholding_algo(data, 5, 18, 0.25), color='orange')

    plt.legend(loc='best')

    plt.show(block=True)




