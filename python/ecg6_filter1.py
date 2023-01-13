#!/usr/bin/python3

import argparse
from datetime import datetime
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import peakutils

from dataclasses import dataclass

from scipy.signal import savgol_filter

parser = argparse.ArgumentParser(description='Analyze Polar H10 ECG data')
parser.add_argument('filename', nargs='?', default="testdata/hr_data_2023-01-13_11-40-07.bin")
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
    record = -1

    while True:
        data_len = int.from_bytes(f.read(4), byteorder='little')
        data = f.read(data_len)
        record += 1

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

    time = np.array(ecg_data.time)
    value = np.array(ecg_data.value)

    # find peaks
    bpm_max = 200                                   # limit at around 200 bpm
    min_dist = int(sampleRate / (bpm_max/60))       # number of samples at 130Hz sampling rate
    print(f"{min_dist}")
    peaks = peakutils.indexes(value, thres=0.75/max(value), min_dist=min_dist)

    # Calculate HR from peaks
    print(f"# peaks: {len(peaks)}")
    last_i = 0
    for i in range(1, len(peaks)):
        # get interval and calculate HR
        interval = time[peaks[i]] - time[peaks[last_i]]
        HR = 60.0*1.0e9/interval

        runtime = datetime.fromtimestamp((time[peaks[last_i]]+interval/2)/1e9) - timestamp_ref
        print(f"Run time: {runtime}, Interval: {interval/1.0e6:.1f} ms, HR: {HR:.1f} 1/min")

        hr_data.time.append(time[peaks[last_i]] + interval/2)
        hr_data.value.append(HR)

        # Next
        last_i = i
    
    fig, ax1 = plt.subplots()
    ax1.plot(hr_data.time, hr_data.value, color='orange')

    window = 21
    order = 2
    y_sf = savgol_filter(hr_data.value, window, order)
    ax1.plot(hr_data.time, y_sf)

    @ticker.FuncFormatter
    def major_formatter(x, pos):
        return str(datetime.fromtimestamp(x/1e9) - timestamp_ref).split('.')[0]

    plt.xticks(rotation=90)
    ax1.xaxis.set_major_formatter(major_formatter)
    #ax2 = ax1.twinx()
    #ax2.plot(ecg_data.time, ecg_data.value)
    
    plt.show(block=True)
