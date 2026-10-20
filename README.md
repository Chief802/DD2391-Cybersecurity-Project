# DD2391-Cybersecurity-Project

## Problem Statement

The goal of the project is to investigate the information passively released by Bluetooth devices, with a focus on Bluetooth Low Energy (BLE) devices. These devices broadcast so called advertisement packages containing various kinds of data without any requirements of authentication to obtain it. This data is often assumed to be anonymous and not to be problematic for nearby observers to obtain. Therefore we investigate how much of the data broadcasted, and passively extracted from a nearby observer, can be used to identify and track the precise location of a specific physical device without its owners knowledge.

## Reference

## Project Documentation

Devices can be tracked and identified by scanning for nearby Bluetooth devices over a 6-second window, extracting broadcast data, distance from the scanner, and identifying the device through given name. Devices are also judged on "privacy", a metric dependent on available information obtained. MAC/UUID addresses, local names, signal strength (RSSI), and Service UUIDs are captured for all BLE devices. Raw company IDs are additionally mapped to know manufacturers, such as Apple, Samsung, Google, and other IoT brands using hardcoded IDs. A log-distance path loss algorithm is used to calculate physical distance to the device using the aforementioned RSSI and TX power. For Apple devices, additional information can be learned by parsing Proximity Pairing, giving information about battery life for individual airbuds, as well as identifying states such as AirDrop or Find My.

We developed and used two scripts to passively obtain broadcasted traffic from nearby BLE device without any specific requirements, such as pairing or have an active connection to the device in question. They only require that bluetooth is activated on the device, and they runs asynchronously.

For bluetoothscanner.py, it scans all nearby BLE devices over a 6-second window, and for each device we extract manufacturer specific data as well as MAC adress, advertised local name, signal strength (RSSI) and advertised service UUIDs. All detected devices are displayed, sorted by signal strength from furthest to closest. Each entry details obtained information about each device. The physical distance to each recorded device is estimated from RSSI and TX power by using a log distance path loss model.

In deviceTracker.py, we can show that the information obtained passively as a nearby observer is enough to track the specific device in question in real time, without any requirements put on the nearby observer to e.g. connect to the device. advertisement are matched by the device MAC adress or device name and are able to smooth the signal via an rolling avergage over the last 50 RSSI readings. This allows us to create a distance estimate to the device which is constantly updated and allows for us to confirm that it is physical present and approximate its location.

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
