import asyncio
import argparse
from collections import deque
from bleak import BleakScanner

RSSI_HISTORY_SIZE=50

async def track_device(target_mac=None, target_name=None):
    identifier = target_mac if target_mac else target_name
    print(f"Looking for device: '{identifier}' ... \n")

    rssi_window = deque(maxlen=RSSI_HISTORY_SIZE)
    print(f"Tracking '{identifier}' ...\n")

    def detection_callback(device, advertisement_data):
        name = device.name or advertisement_data.local_name or "Ej namngiven"
        mac = device.address
        
        match = False
        if target_mac and target_mac.lower() in mac.lower():
            match = True
        elif target_name and target_name.lower() in name.lower():
            match = True

        if match:
            rssi = advertisement_data.rssi
            rssi_window.append(rssi)

            avg_rssi = sum(rssi_window) / len(rssi_window)

            tx_power = -59
            n = 2.5
            try:
                dist = 10 ** ((tx_power - avg_rssi) / (10 * n))
                dist_str = f"~{round(dist, 1)} meters"
            except OverflowError:
                dist_str = "> 50 meters"

            print(f"Found device! [{name} | {mac}] | RSSI (mean): {avg_rssi:.1f} dBm | Distance: {dist_str}", end="\r")

    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()

    try:
        while True:
            await asyncio.sleep(1.0)
    except asyncio.CancelledError:
        pass
    finally:
        await scanner.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mac", type=str)
    parser.add_argument("-n", "--name", type=str)
    
    args = parser.parse_args()

    target_mac = args.mac
    target_name = args.name

    if not target_mac and not target_name:
        print("No device chosen. Specificy device MAC or name using --mac or --name respectively")
        exit(0)

    asyncio.run(track_device(target_mac=target_mac, target_name=target_name))
