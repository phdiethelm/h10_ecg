#!/usr/bin/python3

import asyncio
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

address = "ec:ea:02:85:d9:7a"
PMD_CONTROL = "fb005c81-02e7-f387-1cad-8acd2d8df0c8"
PMD_DATA = "fb005c82-02e7-f387-1cad-8acd2d8df0c8"

def pmd_control_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    hex = [f"{i:02x}" for i in data]
    print(f"CTRL: {hex}")

def pmd_data_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    hex = [f"{i:02x}" for i in data]
    print(f"DATA: {hex}")

async def main():
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")
        
        # Register notifications
        await client.start_notify(PMD_CONTROL, pmd_control_handler)
        await client.start_notify(PMD_DATA, pmd_data_handler)
        
        # Start Stream
        await client.write_gatt_char(PMD_CONTROL, bytearray([0x02, 0x00, 0x00, 0x01, 0x82, 0x00, 0x01, 0x01, 0x0e, 0x00]))
        
        # Wait some time
        await asyncio.sleep(5)
        await client.stop_notify(PMD_DATA)

asyncio.run(main())
