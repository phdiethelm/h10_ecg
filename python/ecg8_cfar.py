#!/usr/bin/python3

import argparse
import os

import numpy as np
import matplotlib.pyplot as plt

from scipy import ndimage

# Lifted from https://tsaith.github.io/detect-peaks-with-cfar-algorithm.html
def detect_peaks(x, num_train, num_guard, rate_fa):
    """
    Detect peaks with CFAR algorithm.
    
    num_train: Number of training cells.
    num_guard: Number of guard cells.
    rate_fa: False alarm rate. 
    """
    num_cells = len(x)
    num_train_half = int(round(num_train / 2))
    num_guard_half = int(round(num_guard / 2))
    num_side = num_train_half + num_guard_half

    alpha = num_train*(rate_fa**(-1/num_train) - 1) # threshold factor
    
    peak_idx = []
    for i in range(num_side, num_cells - num_side):
        
        if i != i-num_side+np.argmax(x[i-num_side:i+num_side+1]): 
            continue
        
        sum1 = np.sum(x[i-num_side:i+num_side+1])
        sum2 = np.sum(x[i-num_guard_half:i+num_guard_half+1]) 
        p_noise = (sum1 - sum2) / num_train 
        threshold = alpha * p_noise
        
        if x[i] > threshold: 
            peak_idx.append(i)
    
    peak_idx = np.array(peak_idx, dtype=int)
    
    return peak_idx


parser = argparse.ArgumentParser(description='Analyze Polar H10 ECG data')
parser.add_argument('filename', nargs='?', default="testdata/hr_data_2023-01-13_11-40-07.bin")
parser.add_argument('reference', nargs='?', default="testdata/Philipp_Diethelm_2023-01-13_11-40-07.csv")
parser.add_argument('ref_add', nargs='?', default=260)
parser.add_argument('ref_cut', nargs='?', default=145)
args = parser.parse_args()

signature = 'H10 ECG v1.0 binary data'.encode('utf8')

with open(args.filename, mode="rb") as f:
    if f.read(len(signature)) != signature:
        print(f"Unknown file format!")
        os._exit(-1)

    print("Reading data...")

    sampleRate = 130
    deltaT_ns = 1e9 / sampleRate

    ecg_time = []
    ecg_value = []
    values = 0

    while True:
        data_len = int.from_bytes(f.read(4), byteorder='little')
        #print(data_len)
        data = f.read(data_len)

        if len(data) != data_len or data_len == 0:
            break
        
        if data[0] == 0x00: # 0x00 = ECG
            time = int.from_bytes(data[1:][0:7], byteorder='little', signed=False)
            i = 9
            sample = 0
            deltaT = 1e9/130.0
            
            frame_type = data[i]
            if frame_type == 0: # 0 = ECG Data
                i += 1
                while len(data[i:][0:3]) == 3:
                    ecg_time.append(time + sample * deltaT)
                    ecg_value.append(int.from_bytes(data[i:][0:2], byteorder='little', signed=True))
                    i += 3
                    sample += 1
        values += 1
        #if values >= 5000:
        #    break


    # ==========================================================================================================
    # Load reference HR captured from 2nd H10
    # ==========================================================================================================
    from numpy import genfromtxt
    ref_data = genfromtxt(args.reference, delimiter=',', skip_header=3)
    ref_HR = ref_data[...,2]
    ref_HR2 = ref_HR
    # Insert or cut at beginning of reference data
    if args.ref_add != None:
        if args.ref_add > 0:
            ref_HR2 = np.insert(ref_HR, 1, [100.0]*(args.ref_add))
        else:
            ref_HR2 = ref_HR[-args.ref_add:]
    # Insert or remove at end of reference data
    if args.ref_cut != None:
        if args.ref_cut > 0:
            ref_HR2 = ref_HR2[:-args.ref_cut]
        else:
            ref_HR2 = np.insert(ref_HR2, 1, [100.0]*(-args.ref_cut))
    #plt.plot(ref_HR2)
    #plt.title("HR directly from H10 #2")
    #plt.axis(ymin=100, ymax=200)
    #plt.savefig(f"CFAR_ref.png")
    #plt.close()

    # ==========================================================================================================
    # CFAR experimentation
    # ==========================================================================================================
    #for train in range(40,80,10):
    for train in [60]:
        #for guard in [10,15,20]:
        for guard in [15]:
            #for rate_fa in [1,1e-1]:
            for rate_fa in [1]:
                print("Peak detection...")
                # find peaks
                peaks = detect_peaks(ecg_value, train, guard, rate_fa)

                # Calculate HR from peaks
                print(f"# peaks: {len(peaks)}")

                last_i = 0
                hr_time = []
                hr_value = []
                hr_time2 = []
                hr_value2 = []
                for i in range(1, len(peaks)):
                    # get interval and calculate HR
                    interval = ecg_time[peaks[i]] - ecg_time[peaks[last_i]]
                    HR = 60.0*1.0e9/interval
                    print(f"Interval: {interval/1.0e6:.1f} ms, HR: {HR:.1f} 1/min")

                    hr_time.append(ecg_time[peaks[last_i]] + interval/2)
                    hr_value.append(HR)

                    # Next
                    last_i = i

                #hr_value_f = ndimage.median_filter(hr_value, size=10)
                def custom_filter(data):
                    return np.average(data)
                hr_value_f = ndimage.generic_filter(hr_value, custom_filter, size=40, mode='mirror')
                print(f"len hr_value_f={len(hr_value_f)}, len hr_value={len(hr_value)}")

                #fig, ax = plt.figure(figsize=(8, 4))

                fig, ax1 = plt.subplots(figsize=(8, 4))
                #ax1.plot(ecg_time, ecg_value)
                #ax1.plot(np.array(ecg_time)[peaks], np.array(ecg_value)[peaks], 'rD')
                ax1 = ax1.twinx()
                ax1.plot(hr_time, hr_value, color='orange', linewidth=0.5, alpha=0.5)
                ax1.plot(hr_time, hr_value_f, color='green', linewidth=0.8)
                ax1.axis(ymin=100, ymax=200)
                ay2 = ax1.twiny()
                ay2.plot(ref_HR2, '--', linewidth=0.5)
                plt.title(f"CFAR: train={train}, guard={guard}, rate_fa={rate_fa}")
                plt.savefig(f"CFAR_{train}_{guard}_{rate_fa}.pdf", dpi=300, bbox_inches="tight", pad_inches=0)
                plt.show(block=True)
                plt.close()

