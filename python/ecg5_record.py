#!/usr/bin/python3

import argparse
import asyncio
import contextvars
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

import numpy as np
import matplotlib.pyplot as plt
from numpy_ringbuffer import RingBuffer
import peakutils

from dataclasses import dataclass

parser = argparse.ArgumentParser(description='Record Polar H10 ECG data')
parser.add_argument('filename', nargs='?', default="hr_data.bin")
parser.add_argument('-a', '--address', default='ec:ea:02:85:d9:7a')
parser.add_argument('-t', '--runtime', default=None, help="Automatically stop recording after X seconds")
parser.add_argument('-dt', '--display-time', default=10, help="Real time display time in seconds")
args = parser.parse_args()

with open(args.filename, mode="wb") as f:
    f.write('H10 ECG v1.0 binary data'.encode('utf8'))

    PMD_CONTROL = "fb005c81-02e7-f387-1cad-8acd2d8df0c8"
    PMD_DATA = "fb005c82-02e7-f387-1cad-8acd2d8df0c8"

    @dataclass
    class xt_data():
        time: None
        value: None

    display_time_s = args.display_time
    sampleRate = 130
    deltaT_ns = 1e9 / sampleRate
    rb_capacity = int(display_time_s * 1e9 / deltaT_ns)

    close_event_var = contextvars.ContextVar('close_event')

    print(f"Ring buffer capacity: {rb_capacity}")

    ecg_data = xt_data(
        time = RingBuffer(capacity=rb_capacity, dtype=np.uint64),
        value = RingBuffer(capacity=rb_capacity, dtype=np.int16))

    peak_data = xt_data(
        time = np.array(1,dtype=np.uint64),
        value = np.array(1,dtype=np.int16))

    plt.ion()
    ecg_data_plot_handle, = plt.plot(ecg_data.time, ecg_data.value)
    peak_data_plot_handle, = plt.plot(peak_data.time, peak_data.value, marker="o", ls="", ms=4)    # Peak markers

    def on_close(event):
        close_event = close_event_var.get()
        close_event.set()
        print('Closed Figure')

    plt.connect('close_event', on_close)

    plot_annotations = []

    def pmd_control_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
        hex = [f"{i:02x}" for i in data]
        print(f"CTRL: {hex}")
        
        # OK
        # CTRL: ['f0', '02', '00', '06', '00']
        #   0xF0 = control point message
        #   0x02 = op_code(Start Measurement)
        #   0x00 = measurement_type(ECG)
        #   0x00 = error(ERROR ALREADY IN STATE)
        #   0x00 = more_frames(false)
        #   0x00 = reserved
        
        # OK (Info)
        # CTRL: ['f0', '02', '00', '00', '00']
        #   0xF0 = control point message
        #   0x02 = op_code(Start Measurement)
        #   0x00 = measurement_type(ECG)
        #   0x00 = error(SUCCESS)
        #   0x00 = more_frames(false)
        #   0x00 = reserved
        
        # Error (MTU too small)
        # CTRL: ['f0', '01', '00', '0a']
        #   0xF0 = control point message
        #   0x01 = op_code(Get Measurement settings)
        #   0x00 = measurement_type(ECG)
        #   0x0a = error(ERROR INVALID MTU)

    def pmd_data_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
        # hex = [f"{i:02x}" for i in data]
        # print(f"DATA: {hex}")

        f.write(int.to_bytes(len(data), length=4, byteorder='little', signed=False))
        f.write(data)
        
        # DATA: ['00', '3a', 'd2', '30', '03', 'c2', '4f', '52', '08', '00', '8b', 'ff', 'ff', '99', 'ff', 'ff', 'ae', 'ff', 'ff', 'a9', 'ff', 'ff', 'a7', 'ff', 'ff', 'c0', 'ff', 'ff', 'bb', 'ff', 'ff', '82', 'ff', 'ff', '41', 'ff', 'ff', '34', 'ff', 'ff', '5b', 'ff', 'ff', '7b', 'ff', 'ff', '7d', 'ff', 'ff', '8b', 'ff', 'ff', '9d', 'ff', 'ff', 'ab', 'ff', 'ff', 'c0', 'ff', 'ff', 'd2', 'ff', 'ff', 'd9', 'ff', 'ff', 'e3', 'ff', 'ff', 'e9', 'ff', 'ff', 'f3', 'ff', 'ff', '0b', '00', '00', '19', '00', '00', '14', '00', '00', '1b', '00', '00', '29', '00', '00', '3b', '00', '00', '5c', '00', '00', '77', '00', '00', '85', '00', '00', '8c', '00', '00', '8e', '00', '00', '8a', '00', '00', '73', '00', '00', '4e', '00', '00', '32', '00', '00', '2b', '00', '00', '29', '00', '00', '2b', '00', '00', '3b', '00', '00', '47', '00', '00', '47', '00', '00', '47', '00', '00', '50', '00', '00', '63', '00', '00', '73', '00', '00', '77', '00', '00', '77', '00', '00', '75', '00', '00', '7c', '00', '00', '8a', '00', '00', '95', '00', '00', '95', '00', '00', '8e', '00', '00', '83', '00', '00', '83', '00', '00', '8c', '00', '00', '91', '00', '00', '91', '00', '00', '8a', '00', '00', '7e', '00', '00', '80', '00', '00', '8e', '00', '00', '9a', '00', '00', '9c', '00', '00', '93', '00', '00', '83', '00', '00', '7a', '00', '00', '85', '00', '00', '91', '00', '00', '8c', '00', '00', '6c', '00', '00']
        #   0x00 = ECG
        #   0x3a, 0xd2, 0x30, 0x03, 0xc2, 0x4f, 0x52, 0x08 = time in ns
        #   0x00 = ECG Frame type
        #   0x8b, 0xff, 0xff, sample 0, negative
        #   0x99, 0xff, 0xff,
        #   0xae, 0xff, 0xff,
        #   0xa9, 0xff, 0xff,
        #   0xa7, 0xff, 0xff,
        #   0xc0, 0xff, 0xff,
        #   0xbb, 0xff, 0xff,
        #   0x82, 0xff, 0xff,
        #   0x41, 0xff, 0xff,
        #   0x34, 0xff, 0xff,
        #   0x5b, 0xff, 0xff,
        #   0x7b, 0xff, 0xff,
        #   0x7d, 0xff, 0xff,
        #   0x8b, 0xff, 0xff,
        #   0x9d, 0xff, 0xff,
        #   0xab, 0xff, 0xff,
        #   0xc0, 0xff, 0xff,
        #   0xd2, 0xff, 0xff,
        #   0xd9, 0xff, 0xff,
        #   0xe3, 0xff, 0xff,
        #   0xe9, 0xff, 0xff,
        #   0xf3, 0xff, 0xff,
        #   0x0b, 0x00, 0x00, sample 22, positive
        #   0x19, 0x00, 0x00, 
        #   0x14, 0x00, 0x00,
        #   0x1b, 0x00, 0x00,
        #   0x29, 0x00, 0x00,
        
        if data[0] == 0x00: # 0x00 = ECG
            time = int.from_bytes(data[1:][0:7], byteorder='little', signed=False)
            i = 9
            sample = 0
            deltaT = 1e9/130.0
            # print(f"{time} {deltaT}")
            frame_type = data[i]
            if frame_type == 0: # 0 = ECG Data
                i += 1
                while len(data[i:][0:3]) == 3:
                    ecg_data.time.append(time + sample * deltaT)
                    ecg_data.value.append(int.from_bytes(data[i:][0:2], byteorder='little', signed=True))
                    i += 3
                    sample += 1
            
            # update line graph data
            value = np.array(ecg_data.value)
            time = np.array(ecg_data.time)
            ecg_data_plot_handle.set_data(time, value)

            # find peaks
            peaks = peakutils.indexes(value, thres=0.75/max(value), min_dist=100)

            # mark peaks in graph
            peak_data_plot_handle.set_data(time[peaks], value[peaks])

            # remove annotations
            for i, a in enumerate(plot_annotations):
                a.remove()
            plot_annotations[:] = []

            # Calculate HR from peaks
            print(f"# peaks: {len(peaks)}")
            last_i = 0
            for i in range(1, len(peaks)):
                # get interval and calculate HR
                interval = time[peaks[i]] - time[peaks[last_i]]
                HR = 60.0*1.0e9/interval
                print(f"Interval: {interval/1.0e6:.1f} ms, HR: {HR:.1f} 1/min")

                # Annotate
                a = plt.annotate(f"{HR:.0f}", xy=(time[peaks[last_i]] + interval/2, max(value[peaks[i]], value[peaks[i]])), ha='center')
                plot_annotations.append(a)

                # Next
                last_i = i

            # Update display
            plt.gca().relim()
            plt.gca().autoscale_view()
            plt.pause(0.01)

    async def main():
        async with BleakClient(args.address) as client:
            close_event = asyncio.Event()
            close_event_var.set(close_event)

            print(f"Connected: {client.is_connected}")
            
            # Register Notifications
            await client.start_notify(PMD_CONTROL, pmd_control_handler)
            await client.start_notify(PMD_DATA, pmd_data_handler)
            
            # Write to PMD control point
            #   0x02 = Start Measurement
            #   0x01 = measurement_type(ECG)
            #   0x00 = setting_type(SAMPLE_RATE)
            #   0x01 = array_length(1)
            #   0x82 0x00 = 130 = 130 Hz
            #   0x01 = setting_type(RESOLUTION)
            #   0x01 = array_length(1)
            #   0x0e = 0x0e 0x00 = 14 = 14 Bits
            await client.write_gatt_char(PMD_CONTROL, bytearray([0x02, 0x00, 0x00, 0x01, 0x82, 0x00, 0x01, 0x01, 0x0e, 0x00]))
            
            if args.runtime != None:
                # Run for some time
                await asyncio.sleep(args.runtime)
            else:
                # Run until window is closed
                await close_event.wait()
            
            # Write to PMD control point
            #   0x03 = Stop Measurement
            #   0x01 = measurement_type(ECG)
            await client.write_gatt_char(PMD_CONTROL, bytearray([0x03, 0x00]))
            
            # Cleanup
            await client.stop_notify(PMD_DATA)
            await client.stop_notify(PMD_CONTROL)


    asyncio.run(main())

    plt.show(block=True)
