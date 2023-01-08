# Exploration with linux tools

Environment
```
$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 22.04.1 LTS
Release:	22.04
Codename:	jammy
```

## Setup 

Add the following lines to /etc/bluetooth/main.conf:
```
[Genrral]
# Enable Low Energy support. Default is false.
EnableLE = true
# Enable the GATT attribute server. Default is false.
AttributeServer = true
DisablePlugins=pnat
```

## Find the device
```
$ sudo bluetoothctl
Agent registered
[CHG] Controller 8C:F8:C5:76:84:F4 Pairable: yes
[bluetooth]# scan le
Discovery started
[CHG] Controller 8C:F8:C5:76:84:F4 Discovering: yes
[NEW] Device EC:EA:02:85:D9:7A Polar H10 8AA87D20
[bluetooth]# scan off
Discovery stopped
[CHG] Device EC:EA:02:85:D9:7A TxPower is nil
[CHG] Device EC:EA:02:85:D9:7A RSSI is nil
[CHG] Controller 8C:F8:C5:76:84:F4 Discovering: no
[bluetooth]# exit
$
```

## Gatttool

Start ```gatttool``` in interactive mode

```
$ gatttool -t random -b EC:EA:02:85:D9:7A -I
```

### Connect to H10
```
[EC:EA:02:85:D9:7A][LE]> connect
Attempting to connect to EC:EA:02:85:D9:7A
Connection successful
```

### Query some information
```
[EC:EA:02:85:D9:7A][LE]> primary
attr handle: 0x0001, end grp handle: 0x0009 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x000a, end grp handle: 0x000d uuid: 00001801-0000-1000-8000-00805f9b34fb
attr handle: 0x000e, end grp handle: 0x0013 uuid: 0000180d-0000-1000-8000-00805f9b34fb
attr handle: 0x0014, end grp handle: 0x002b uuid: 0000181c-0000-1000-8000-00805f9b34fb
attr handle: 0x002c, end grp handle: 0x003a uuid: 0000180a-0000-1000-8000-00805f9b34fb
attr handle: 0x003b, end grp handle: 0x003e uuid: 0000180f-0000-1000-8000-00805f9b34fb
attr handle: 0x003f, end grp handle: 0x0044 uuid: 6217ff4b-fb31-1140-ad5a-a45545d7ecf3
attr handle: 0x0045, end grp handle: 0x004b uuid: fb005c80-02e7-f387-1cad-8acd2d8df0c8
attr handle: 0x004c, end grp handle: 0xffff uuid: 0000feee-0000-1000-8000-00805f9b34fb
```

```
[EC:EA:02:85:D9:7A][LE]> char-desc
handle: 0x0001, uuid: 00002800-0000-1000-8000-00805f9b34fb                      # Primary Service
handle: 0x0002, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0003, uuid: 00002a00-0000-1000-8000-00805f9b34fb                      # Device Name
handle: 0x0004, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0005, uuid: 00002a01-0000-1000-8000-00805f9b34fb                      # Appearance
handle: 0x0006, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0007, uuid: 00002a04-0000-1000-8000-00805f9b34fb                      # Peripheral Preferred Connection Parameters
handle: 0x0008, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0009, uuid: 00002aa6-0000-1000-8000-00805f9b34fb                      # Central Address Resolution

handle: 0x000a, uuid: 00002800-0000-1000-8000-00805f9b34fb                      # Primary Service
handle: 0x000b, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x000c, uuid: 00002a05-0000-1000-8000-00805f9b34fb                      # Service Changed
handle: 0x000d, uuid: 00002902-0000-1000-8000-00805f9b34fb                      # Client Characteristic Configuration

handle: 0x000e, uuid: 00002800-0000-1000-8000-00805f9b34fb                      # Primary Service
handle: 0x000f, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0010, uuid: 00002a37-0000-1000-8000-00805f9b34fb                      # Heart Rate Measurement characteristic UUID
handle: 0x0011, uuid: 00002902-0000-1000-8000-00805f9b34fb                      # Client Characteristic Configuration
handle: 0x0012, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0013, uuid: 00002a38-0000-1000-8000-00805f9b34fb                      # Body Sensor Location

handle: 0x0014, uuid: 00002800-0000-1000-8000-00805f9b34fb                      # Primary Service
handle: 0x0015, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0016, uuid: 00002a99-0000-1000-8000-00805f9b34fb                      # Database Change Increment
handle: 0x0017, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0018, uuid: 00002a9a-0000-1000-8000-00805f9b34fb                      # User Index
handle: 0x0019, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x001a, uuid: 00002a9f-0000-1000-8000-00805f9b34fb                      # User Control Point
handle: 0x001b, uuid: 00002902-0000-1000-8000-00805f9b34fb                      # Client Characteristic Configuration
handle: 0x001c, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x001d, uuid: 00002a8a-0000-1000-8000-00805f9b34fb                      # First Name
handle: 0x001e, uuid: 00002900-0000-1000-8000-00805f9b34fb                      # Characteristic Extended Properties
handle: 0x001f, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0020, uuid: 00002a90-0000-1000-8000-00805f9b34fb                      # Last Name
handle: 0x0021, uuid: 00002900-0000-1000-8000-00805f9b34fb                      # Characteristic Extended Properties
handle: 0x0022, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0023, uuid: 00002a80-0000-1000-8000-00805f9b34fb                      # Age
handle: 0x0024, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0025, uuid: 00002a8c-0000-1000-8000-00805f9b34fb                      # Gender
handle: 0x0026, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0027, uuid: 00002a98-0000-1000-8000-00805f9b34fb                      # Weight
handle: 0x0028, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0029, uuid: 00002a8e-0000-1000-8000-00805f9b34fb                      # Height
handle: 0x002a, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x002b, uuid: 00002aa2-0000-1000-8000-00805f9b34fb                      # Language
handle: 0x002c, uuid: 00002800-0000-1000-8000-00805f9b34fb                      # Primary Service
handle: 0x002d, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x002e, uuid: 00002a29-0000-1000-8000-00805f9b34fb                      # Manufacturer Name String
handle: 0x002f, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0030, uuid: 00002a24-0000-1000-8000-00805f9b34fb                      # Model Number String
handle: 0x0031, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0032, uuid: 00002a25-0000-1000-8000-00805f9b34fb                      # Serial Number String
handle: 0x0033, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0034, uuid: 00002a27-0000-1000-8000-00805f9b34fb                      # Hardware Revision String
handle: 0x0035, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0036, uuid: 00002a26-0000-1000-8000-00805f9b34fb                      # Firmware Revision String
handle: 0x0037, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0038, uuid: 00002a28-0000-1000-8000-00805f9b34fb                      # Software Revision String
handle: 0x0039, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x003a, uuid: 00002a23-0000-1000-8000-00805f9b34fb                      # System ID

handle: 0x003b, uuid: 00002800-0000-1000-8000-00805f9b34fb                      # Primary Service
handle: 0x003c, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x003d, uuid: 00002a19-0000-1000-8000-00805f9b34fb                      # Battery Level
handle: 0x003e, uuid: 00002902-0000-1000-8000-00805f9b34fb                      # Client Characteristic Configuration

handle: 0x003f, uuid: 00002800-0000-1000-8000-00805f9b34fb                      # Primary Service
handle: 0x0040, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0041, uuid: 6217ff4c-c8ec-b1fb-1380-3ad986708e2d                      # Vendor undocumented
handle: 0x0042, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic
handle: 0x0043, uuid: 6217ff4d-91bb-91d0-7e2a-7cd3bda8a1f3                      # Vendor undocumented
handle: 0x0044, uuid: 00002902-0000-1000-8000-00805f9b34fb                      # Client Characteristic Configuration

handle: 0x0045, uuid: 00002800-0000-1000-8000-00805f9b34fb                      # Primary Service
handle: 0x0046, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic

handle: 0x0047, uuid: fb005c81-02e7-f387-1cad-8acd2d8df0c8                      # Polar: PMD Control Point
handle: 0x0048, uuid: 00002902-0000-1000-8000-00805f9b34fb                      # Client Characteristic Configuration
handle: 0x0049, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic

handle: 0x004a, uuid: fb005c82-02e7-f387-1cad-8acd2d8df0c8                      # Polar: PMD Data MTU Characteristic
handle: 0x004b, uuid: 00002902-0000-1000-8000-00805f9b34fb                      # Client Characteristic Configuration
handle: 0x004c, uuid: 00002800-0000-1000-8000-00805f9b34fb                      # Primary Service
handle: 0x004d, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic

handle: 0x004e, uuid: fb005c51-02e7-f387-1cad-8acd2d8df0c8                      # Vendor undocumented
handle: 0x004f, uuid: 00002902-0000-1000-8000-00805f9b34fb                      # Client Characteristic Configuration
handle: 0x0050, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic

handle: 0x0051, uuid: fb005c52-02e7-f387-1cad-8acd2d8df0c8                      # Vendor undocumented
handle: 0x0052, uuid: 00002902-0000-1000-8000-00805f9b34fb                      # Client Characteristic Configuration
handle: 0x0053, uuid: 00002803-0000-1000-8000-00805f9b34fb                      # Characteristic

handle: 0x0054, uuid: fb005c53-02e7-f387-1cad-8acd2d8df0c8                      # Vendor undocumented
```

### Read features from device
```
[EC:EA:02:85:D9:7A][LE]> char-read-uuid fb005c81-02e7-f387-1cad-8acd2d8df0c8
handle: 0x0047 	 value: 0f 05 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
```

Deconding of response:
| Response | Byte(s) | Bit(s) | Description                         |
| -------- | ------- | ------ | ----------------------------------- |
| 0x0f     | 0       | 7..0   | control point feature read response |
| 0x05     | 1       | 7..0   | PMD measurement types               |
|          |         | 0      | ecg_supported = true                |
|          |         | 1      | ppg_supported = false               |
|          |         | 2      | acc_supported = true                |
|          |         | 3      | ppi_supported = false               |
|          |         | 4      | rfu = false                         |
|          |         | 5      | gyro_supported = false              |
|          |         | 6      | mag_supported = false               |
| 0x00     | 2+      |        | Unknown                             |


### Enable Notification and/or Indication
Extracted from further down the spec. near Table 3.11 in the specification
| Configuration | Value  | Description                                                                                                                        |
| ------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| Notification  | 0x0001 | The Characteristic Value shall be notified.This value can only be set if the characteristic's property has the notify bit set.     |
| Indication    | 0x0002 | The Characteristic Value shall be indicated. This value can only be set if the characteristic's property has the indicate bit set. |

```
[EC:EA:02:85:D9:7A][LE]> char-write-req 0x48 0300
Characteristic value was written successfully
```

```
[EC:EA:02:85:D9:7A][LE]> char-write-req 0x48 0200
Characteristic value was written successfully
```

```
[EC:EA:02:85:D9:7A][LE]> char-write-req 0x48 0100
Characteristic value was written successfully
```

### Get measurement settings

Request
| Byte(s) | Request | Description              |
| ------- | ------- | ------------------------ |
| 0       | 0x01    | Get measurement settings |
| 1       | 0x00    | measurement_type(ECG)    |

```
[EC:EA:02:85:D9:7A][LE]> char-write-req 0x47 0101
Characteristic value was written successfully
Indication   handle = 0x0047 value: f0 00 01 0a 
```
Response
| Byte(s) | Response | Description                       |
| ------- | -------- | --------------------------------- |
| 0       | 0xf0     | control point message             |
| 1       | 0x01     | op_code(Get Measurement settings) |
| 2       | 0x00     | measurement_type(ECG)             |
| 3       | 0x0a     | error(ERROR INVALID MTU)          |


### Increase MTU
```
[EC:EA:02:85:D9:7A][LE]> mtu 256
MTU was exchanged successfully: 232
```

### Retry
Request
| Byte(s) | Request | Description              |
| ------- | ------- | ------------------------ |
| 0       | 0x01    | Get measurement settings |
| 1       | 0x00    | measurement_type(ECG)    |

```
[EC:EA:02:85:D9:7A][LE]> char-write-req 0x47 0101
Characteristic value was written successfully
Indication   handle = 0x0047 value: f0 01 00 00 00 00 01 82 00 01 01 0e 00
```

Response
| Byte(s) | Response  | Description                       |
| ------- | --------- | --------------------------------- |
| 0       | 0xf0      | control point message             |
| 1       | 0x01      | op_code(Get Measurement settings) |
| 2       | 0x00      | measurement_type(ECG)             |
| 3       | 0x00      | error(SUCCESS)                    |
| 4       | 0x00      | more_frames(false)                |
| 5       | 0x00      | setting_type(SAMPLE_RATE)         |
| 6       | 0x01      | array_length(1)                   |
| 7..8    | 0x82 0x00 | 0x0082 = 130 = 130 Hz             |
| 9       | 0x01      | setting_type(RESOLUTION)          |
| 10      | 0x01      | array_length(1)                   |
| 11..12  | 0x0e 0x00 | 0x000e = 14 = 14 Bits             |


### Trying to start Measurement

Request
| Byte(s) | Request | Description              |
| ------- | ------- | ------------------------ |
| 0       | 0x02    | Get measurement settings |
| 1       | 0x00    | measurement_type(ECG)    |

```
char-write-req 0x47 0200
Characteristic value was written successfully
Indication   handle = 0x0047 value: f0 02 00 05 00 
```

Response
| Byte(s) | Response | Description                    |
| ------- | -------- | ------------------------------ |
| 0       | 0xf0     | control point message          |
| 1       | 0x02     | op_code(Start Measurement)     |
| 2       | 0x00     | measurement_type(ECG)          |
| 3       | 0x05     | error(ERROR INVALID PARAMETER) |


### Trying to start Measurement
Combining start measurement with information received by get measurement settings...

Request
| Byte(s) | Response  | Description                |
| ------- | --------- | -------------------------- |
| 0       | 0xf0      | control point message      |
| 1       | 0x02      | op_code(Start Measurement) |
| 2       | 0x00      | measurement_type(ECG)      |
| 3       | 0x00      | setting_type(SAMPLE_RATE)  |
| 4       | 0x01      | array_length(1)            |
| 5..6    | 0x82 0x00 | 0x0082 = 130 = 130 Hz      |
| 7       | 0x01      | setting_type(RESOLUTION)   |
| 8       | 0x01      | array_length(1)            |
| 9..10   | 0x0e 0x00 | 0x000e = 14 = 14 Bits      |

```
char-write-req 0x47 02000001820001010e00
Characteristic value was written successfully
Indication   handle = 0x0047 value: f0 02 00 00 00 00
```
Response
| Byte(s) | Response | Description                |
| ------- | -------- | -------------------------- |
| 0       | 0xF0     | control point message      |
| 1       | 0x02     | op_code(Start Measurement) |
| 2       | 0x00     | measurement_type(ECG)      |
| 3       | 0x00     | error(SUCCESS)             |
| 4       | 0x00     | more_frames(false)         |
| 5       | 0x00     | reserved                   |


### ECG Data stream!
Its alive!

```
Notification handle = 0x004a value: 00 91 f7 70 aa 30 49 52 08 00 7a 00 00 67 00 00 83 00 00 ac 00 00 ac 00 00 a1 00 00 a5 00 00 a1 00 00 a8 00 00 ac 00 00 9a 00 00 91 00 00 75 00 00 32 00 00 df 00 00 94 03 00 39 07 00 b9 08 00 07 06 00 52 01 00 fa fe ff 64 ff ff ab ff ff 5f ff ff 7d ff ff a2 ff ff 8d ff ff 76 ff ff 64 ff ff 79 ff ff 9d ff ff a2 ff ff b0 ff ff c7 ff ff d5 ff ff ec ff ff f0 ff ff e7 ff ff ec ff ff ec ff ff ee ff ff fe ff ff fa ff ff f7 ff ff 00 00 00 f7 ff ff f7 ff ff 06 00 00 f7 ff ff d7 ff ff be ff ff ab ff ff a7 ff ff b7 ff ff c0 ff ff bb ff ff c9 ff ff dc ff ff dc ff ff ec ff ff fc ff ff f0 ff ff e7 ff ff e5 ff ff de ff ff d7 ff ff d9 ff ff d7 ff ff d0 ff ff d7 ff ff e5 ff ff ec ff ff ec ff ff 
Notification handle = 0x004a value: 00 7c 3b de cb 30 49 52 08 00 ee ff ff f5 ff ff f5 ff ff f5 ff ff 00 00 00 02 00 00 e3 ff ff a0 ff ff 7b ff ff 9b ff ff b9 ff ff be ff ff c7 ff ff ce ff ff c5 ff ff c9 ff ff d5 ff ff c2 ff ff b0 ff ff a9 ff ff 8d ff ff 80 ff ff 9b ff ff b0 ff ff b0 ff ff b7 ff ff cc ff ff dc ff ff dc ff ff e0 ff ff e9 ff ff e7 ff ff f3 ff ff 02 00 00 0b 00 00 0d 00 00 02 00 00 fe ff ff 1b 00 00 30 00 00 29 00 00 24 00 00 1b 00 00 10 00 00 1d 00 00 32 00 00 30 00 00 20 00 00 0d 00 00 00 00 00 0d 00 00 24 00 00 34 00 00 37 00 00 24 00 00 1b 00 00 32 00 00 47 00 00 4c 00 00 4c 00 00 3e 00 00 20 00 00 f3 ff ff 09 00 00 39 01 00 0e 04 00 2d 07 00 40 07 00 2a 03 00 51 ff ff 13 ff ff b2 ff ff 3a ff ff 
Notification handle = 0x004a value: 00 ad 57 4b ed 30 49 52 08 00 26 ff ff 8d ff ff 97 ff ff 92 ff ff b0 ff ff a4 ff ff 8d ff ff 9b ff ff ab ff ff a4 ff ff 72 ff ff 44 ff ff 5d ff ff 6f ff ff 4f ff ff 58 ff ff 79 ff ff 80 ff ff 8d ff ff a4 ff ff be ff ff d5 ff ff cc ff ff b9 ff ff c9 ff ff de ff ff c7 ff ff b0 ff ff a7 ff ff 9b ff ff a4 ff ff b4 ff ff cc ff ff f0 ff ff 00 00 00 fe ff ff 0d 00 00 1b 00 00 14 00 00 00 00 00 f0 ff ff ec ff ff e7 ff ff ec ff ff fa ff ff f0 ff ff e9 ff ff 04 00 00 10 00 00 09 00 00 14 00 00 17 00 00 0b 00 00 14 00 00 24 00 00 29 00 00 2b 00 00 29 00 00 22 00 00 22 00 00 2b 00 00 34 00 00 37 00 00 39 00 00 42 00 00 45 00 00 40 00 00 3b 00 00 42 00 00 55 00 00 59 00 00 42 00 00 24 00 00 
Notification handle = 0x004a value: 00 54 c3 b8 0e 31 49 52 08 00 24 00 00 32 00 00 37 00 00 37 00 00 37 00 00 39 00 00 1d 00 00 f0 ff ff ee ff ff 04 00 00 09 00 00 19 00 00 1b 00 00 e0 ff ff a7 ff ff c9 ff ff ec ff ff e9 ff ff f7 ff ff fc ff ff f7 ff ff 02 00 00 09 00 00 02 00 00 10 00 00 22 00 00 2b 00 00 32 00 00 34 00 00 37 00 00 34 00 00 27 00 00 2b 00 00 3b 00 00 37 00 00 34 00 00 42 00 00 49 00 00 45 00 00 3b 00 00 04 00 00 de ff ff f1 00 00 07 04 00 80 07 00 04 08 00 7f 04 00 34 00 00 b9 fe ff 3a ff ff 4d ff ff 1c ff ff 58 ff ff 84 ff ff 76 ff ff 89 ff ff ab ff ff a9 ff ff ab ff ff c7 ff ff c2 ff ff c0 ff ff dc ff ff cc ff ff ab ff ff cc ff ff ee ff ff e5 ff ff e3 ff ff ec ff ff f0 ff ff e9 ff ff c9 ff ff 
Notification handle = 0x004a value: 00 01 2f 26 30 31 49 52 08 00 b4 ff ff d5 ff ff f0 ff ff e5 ff ff c0 ff ff 84 ff ff 6b ff ff 89 ff ff 8d ff ff 89 ff ff ae ff ff d0 ff ff de ff ff 00 00 00 22 00 00 1d 00 00 04 00 00 04 00 00 10 00 00 09 00 00 fc ff ff fe ff ff ec ff ff d7 ff ff e5 ff ff f5 ff ff f5 ff ff 04 00 00 09 00 00 06 00 00 1d 00 00 34 00 00 2b 00 00 14 00 00 14 00 00 27 00 00 32 00 00 2e 00 00 24 00 00 29 00 00 39 00 00 40 00 00 42 00 00 4e 00 00 47 00 00 30 00 00 34 00 00 4e 00 00 63 00 00 65 00 00 60 00 00 59 00 00 4e 00 00 4c 00 00 47 00 00 3e 00 00 42 00 00 40 00 00 37 00 00 49 00 00 69 00 00 6c 00 00 65 00 00 5c 00 00 3b 00 00 29 00 00 47 00 00 5e 00 00 55 00 00 4c 00 00 57 00 00 65 00 00 6c 00 00 
Notification handle = 0x004a value: 00 aa 9a 93 51 31 49 52 08 00 75 00 00 73 00 00 63 00 00 5e 00 00 77 00 00 8c 00 00 8c 00 00 85 00 00 7c 00 00 83 00 00 98 00 00 9c 00 00 8e 00 00 57 00 00 fc ff ff f5 ff ff 30 00 00 37 00 00 27 00 00 04 00 00 d0 ff ff 7a 00 00 0a 03 00 9f 06 00 52 08 00 eb 05 00 4b 01 00 c7 fe ff 26 ff ff 92 ff ff 3f ff ff 4f ff ff 90 ff ff 90 ff ff 94 ff ff b2 ff ff d5 ff ff e5 ff ff e3 ff ff f5 ff ff 09 00 00 0d 00 00 19 00 00 19 00 00 04 00 00 fc ff ff 0b 00 00 2b 00 00 30 00 00 1d 00 00 12 00 00 24 00 00 42 00 00 45 00 00 22 00 00 0b 00 00 f7 ff ff b7 ff ff 9d ff ff c7 ff ff d0 ff ff c5 ff ff e3 ff ff 00 00 00 0b 00 00 24 00 00 42 00 00 45 00 00 32 00 00 2b 00 00 32 00 00 34 00 00 27 00 00 
```
Notification
| Byte(s) | Response                                | Description               |
| ------- | --------------------------------------- | ------------------------- |
| 0       | 0x00                                    | ECG                       |
| 1..8    | 0xaa 0x9a 0x93 0x51 0x31 0x49 0x52 0x08 | Timestamp (in ns)         |
| 9       | 0x00                                    | frame_type(ECG)           |
| 10..12  | 0x75 0x00 0x00                          | Sample 0: 0x000075  = 117 |
| 13..15  | 0x73 0x00 0x00                          | Sample 1: 0x000073 =  115 |
| ...     |                                         |                           |
| 52..54  | 0xfc 0xff 0xff                          | Sample 14: 0xfffffc = -4  |
| ...     |                                         |                           |


### Stop stream

Request
| Byte(s) | Request | Description           |
| ------- | ------- | --------------------- |
| 0       | 0x03    | Stop measurement      |
| 1       | 0x00    | measurement_type(ECG) |

```
[EC:EA:02:85:D9:7A][LE]> char-write-req 0x47 0300
Characteristic value was written successfully
```

### Disable Notification and/or Indication
```
[EC:EA:02:85:D9:7A][LE]> char-write-req 0x4b 0000
Characteristic value was written successfully
``` 
