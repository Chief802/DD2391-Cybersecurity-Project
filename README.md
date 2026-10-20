# DD2391-Cybersecurity-Project

## Problem Statement

The goal of the project is to investigate the information passively released by Bluetooth devices, with a focus on Bluetooth Low Energy (BLE) devices.

## Reference

## Project Documentation

Devices can be tracked and identified by scanning for active Bluetooth connections over a 6-second window, extracting broadcast data, distance from the scanner, and identifying the device through given name. Devices are also judged on "privacy", a metric dependent on available information obtained. MAC/UUID addresses, local names, signal strength (RSSI), and Service UUIDs are captured for all BLE devices. Raw company IDs are additionally mapped to know manufacturers, such as Apple, Samsung, Google, and other IoT brands using hardcoded IDs. A log-distance path loss algorithm is used to calculate physical distance to the device using the aforementioned RSSI and TX power. For Apple devices, additional information can be learned by parsing Proximity Pairing, giving information about battery life for individual airbuds, as well as identifying states such as AirDrop or Find My.

The script runs asynchronously and requires the used device to have Bluetooth activated. All detected devices are displayed, sorted by signal strength from furthest to closest. Each entry details obtained information about each device. 

Python v3.7 or higher is needed for asyncio, as well as bleak for connecting to BLE devices.

## Project Testing

Testing was performed to assess the accuracy of device distance. A scanner device was placed 1.0m away from a device to be scanned, without physical objects in the way. Tests were performed 10 times to assess accuracy. The individual results for Signal Strength and Estimated Distance are shown in the table below.

| Signal Strength (dBm) | Estimated Distance (m) |
| :--- | :--- |
| -62 | 1.3 |
| -63 | 1.4 |
| -56 | 0.8 |
| -59 | 1.0 |
| -61 | 1.2 |
| -63 | 1.4 |
| -60 | 1.1 |
| -61 | 1.2 |
| -67 | 2.1 |
| -62 | 1.3 |

The results show a mean distance of 1.28m, with a  population standard deviation at 0.325m. Overall, this suggests a rather large error. The program generally shows an object as being further away than it is, with extremes at 0.8 on the lower and at 2.1 at the highest end.
