#!/usr/bin/python3

import argparse
from datetime import datetime
import os

import numpy as np
import matplotlib.pyplot as plt
import peakutils

from dataclasses import dataclass
from scipy.signal import *

parser = argparse.ArgumentParser(description='Analyze Polar H10 ECG data')
parser.add_argument('filename', nargs='?', default="testdata/hr_data_2023-01-13_11-40-07.bin")
parser.add_argument('reference', nargs='?', default="testdata/Philipp_Diethelm_2023-01-13_11-40-07.csv")
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
                while len(data[i:][0:3]) == 3:
                    ecg_data.time.append(timestamp + sample * deltaT)
                    ecg_data.value.append(int.from_bytes(data[i:][0:2], byteorder='little', signed=True))
                    i += 3
                    sample += 1

    time = np.array(ecg_data.time)
    value = np.array(ecg_data.value)

    # Test median filter values
    plt.subplots(1, 3)
    plt.subplot(3, 1, 1)
    for i in [9, 13, 15, 17]:
        plt.plot(medfilt(value, i), linewidth=0.5, label=f"{i}")

    plt.legend(loc="best")
    plt.title("Median Filter kernel sizes")

    # Align toward zero
    value_f = value - medfilt(value, 13)

    plt.subplot(3, 1, 2)
    plt.plot(value_f)
    plt.title("0 aligned Signal")

    # Clip peaks
    value_f2 = np.clip(value_f-300, 0, 1)

    plt.subplot(3, 1, 3)
    plt.plot(value_f2)
    plt.title("Clipped Peaks")
    plt.tight_layout()
    plt.show(block=True)

    # find peaks
    bpm_max = 200                                   # limit at around 200 bpm
    min_dist = int(sampleRate / (bpm_max/60))       # number of samples at 130Hz sampling rate
    print(f"{min_dist}")
    peaks = peakutils.indexes(value_f2, thres=0.5/max(value_f2), min_dist=min_dist)

    # Calculate HR from peaks
    print(f"# peaks: {len(peaks)}")
    last_i = 0
    last_HR = None
    for i in range(1, len(peaks)):
        # get interval and calculate HR
        interval = time[peaks[i]] - time[peaks[last_i]]
        HR = 60.0*1.0e9/interval

        runtime = datetime.fromtimestamp((time[peaks[last_i]]+interval/2)/1e9) - timestamp_ref
        print(f"Run time: {runtime}, Interval: {interval/1.0e6:.1f} ms, HR: {HR:.1f} 1/min")

        # Filter HR variations > 5%
        if last_HR != None:
            if HR > 1.05 *last_HR or HR < 0.95*last_HR:
                HR = last_HR

        hr_data.time.append(time[peaks[last_i]] + interval/2)
        hr_data.value.append(HR)

        # Next
        last_i = i
        last_HR = HR

    # Smoothing tests
    plt.subplots(1, 2)
    plt.subplot(2, 1, 1)
    plt.plot(hr_data.value, linewidth=0.1)
    for N in [3, 7, 15]:
        plt.plot(np.convolve(hr_data.value, np.ones(N), mode='same')/N, linewidth=0.5, label=f"filter {N}")
    plt.legend(loc="best")
    plt.title("HR extracted from ECG (H10 #1)")

    # Load reference HR captured from 2nd H10
    plt.subplot(2, 1, 2)
    from numpy import genfromtxt
    ref_data = genfromtxt(args.reference, delimiter=',', skip_header=3)
    ref_HR = ref_data[...,2]
    plt.plot(ref_HR)
    plt.title("HR directly from H10 #2")
    plt.tight_layout()
    plt.show(block=True)
