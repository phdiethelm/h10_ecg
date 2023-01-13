#!/usr/bin/python3

import argparse
from datetime import datetime
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import peakutils

from dataclasses import dataclass

parser = argparse.ArgumentParser(description='Analyze Polar H10 ECG data')
#parser.add_argument('filename', nargs='?', default="testdata/hr_data_2023-01-13_11-40-07.bin")
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
    
    spectrogram = []
    fft_size = 2048
    values = np.array(ecg_data.value)
    spec_steps = 16
    num_specs = int(len(values) / spec_steps)
    for i in range(0, num_specs):
        d = values[i*spec_steps::][0:fft_size]
        if len(d) != fft_size:
            break
        PSD = np.abs(np.fft.fft(d)**2) # / (fft_size*sampleRate)
        PSD_log = 10.0 * np.log10(PSD)
        PSD_shifted = np.fft.fftshift(PSD_log)
        spectrogram.append(PSD_shifted[int(fft_size/2)::])

    plt.imshow(np.transpose(spectrogram), aspect='auto', origin='lower', extent = [0, len(spectrogram), 0, sampleRate/2*60])
    plt.show(block=True)
