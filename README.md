# DD2391-Cybersecurity-Project

## Problem Statement

The goal of the project is to investigate the information passively released by Bluetooth devices, with a focus on Bluetooth Low Energy (BLE) devices.

## Reference

## Project Documentation

Devices can be tracked and identified by scanning for active Bluetooth connections over a 6-second window, extracting broadcast data, distance from the scanner, and identifying the device through given name. Devices are also judged on "privacy", a metric dependent on available information obtained. MAC/UUID addresses, local names, signal strength (RSSI), and Service UUIDs are captured for all BLE devices. Raw company IDs are additionally mapped to know manufacturers, such as Apple, Samsung, Google, and other IoT brands using hardcoded IDs. A log-distance path loss algorithm is used to calculate physical distance to the device using the aforementioned RSSI and TX power. For Apple devices, additional information can be learned by parsing Proximity Pairing, giving information about battery life for individual airbuds, as well as identifying states such as AirDrop or Find My.

The script runs asynchronously and requires the used device to have Bluetooth activated. All detected devices are displayed, sorted by signal strength from furthest to closest. Each entry details obtained information about each device. 

Python v3.7 or higher is needed for asyncio, as well as bleak for connecting to BLE devices.

## Project Testing

