import asyncio
import argparse
from collections import deque
from bleak import BleakScanner
from bluetooth_numbers import company


# Calculate distance using Log-distance path loss model
def estimate_distance(rssi, n):
    if rssi is None or rssi == 0:
        return "Unkown"

    tx_power = -59

    try:
        dist = 10 ** ((tx_power - rssi) / (10 *n))
        return f"~{round(dist, 1)} meters"
    except OverflowError:
        return "> 50.0"

# Get manufacturer from database
def check_manufacturer(manufacturer_data):
    m_list = []
    if manufacturer_data:
        for comp_id in manufacturer_data.keys():
            comp_name = company.get(comp_id, f"Unknown (ID: {comp_id})")
            m_list.append(comp_name)
    manufacturer_str = ", ".join(m_list) if m_list else "No manufacturer data"
    return manufacturer_str

async def scan_all_devices(n=2.5):
    devices_data = await BleakScanner.discover(timeout=6.0, return_adv=True)
    
    parsed_devices = []

    for device, adv in devices_data.values():
        name = device.name or adv.local_name or "Unknown"
        
        m_list = []
        raw_m_data = {}
        apple_info = ""

        m_str = check_manufacturer(adv.manufacturer_data)
        tx_pwr = adv.tx_power
        dist = estimate_distance(adv.rssi, n)
        

        parsed_devices.append({
            "address": device.address,
            "name": name,
            "rssi": adv.rssi,
            "manufacturer": m_str,
            "apple_info": apple_info,
            "raw_m_data": raw_m_data,
            "uuids": list(adv.service_uuids),
            "tx_power": tx_pwr,
            "distance": dist,
        })

    # SORTERING: Längst bort först -> Närmast längst ner
    parsed_devices.sort(key=lambda x: x["rssi"], reverse=False)

    print("\n" + "="*70)
    print(" Scanning Results (Order: Descending Distance)")
    print("="*70 + "\n")

    for d in parsed_devices:
        print(f"  MAC/UUID:      {d['address']}")
        print(f"  Name:          {d['name']}")
        print(f"  Signal Strench:  {d['rssi']} dBm  (Estimated Distance: {d['distance']})")
        print(f"  Manufacturer:   {d['manufacturer']}")
        
        if d['tx_power'] is not None:
            print(f"  TX Power:      {d['tx_power']} dBm")
        if d['raw_m_data']:
            print(f"  Raw data (Hex):  {d['raw_m_data']}")
            
        print("-" * 60)

    # SAMMANFATTNING
    total_found = len(parsed_devices)
    named_count = sum(1 for d in parsed_devices if d['name'] != "Unknown")

    print("\n" + "="*70)
    print(" Summary")
    print("="*70)
    print(f"# of discovered devices: {total_found}")
    print(f"# of discovered device names: {named_count} av {total_found}")
    print(f"Nearby devices (RSSI > -70 dBm): {sum(1 for d in parsed_devices if d['rssi'] > -70)}")
    print("\n" + "-"*70)

async def track_device(target_mac=None, target_name=None, rssi_history_size=20, n=2.5):
    identifier = target_mac if target_mac else target_name
    print(f"Tracking '{identifier}' ...\n")

    rssi_window = deque(maxlen=rssi_history_size)

    header = f"{'Device Name':<30} | {'MAC / UUID':<36} | {'Manufacturer':<25} | {'RSSI (mean)':<12} | {'Distance':<15}"
    print(header)
    print("-" * len(header))

    def detection_callback(device, advertisement_data):
        name = device.name or advertisement_data.local_name or "Unknown"
        mac = device.address

        manufacturer_str = check_manufacturer(advertisement_data.manufacturer_data)


        match = False
        if target_mac and target_mac.lower() in mac.lower():
            match = True
        elif target_name and target_name.lower() in name.lower():
            match = True

        if match:
            rssi = advertisement_data.rssi
            if rssi is None:
                return

            rssi_window.append(rssi)

            avg_rssi = sum(rssi_window) / len(rssi_window)
            dist_str = estimate_distance(avg_rssi, n)


            print(f"{name:<30} | {mac:<36} | {manufacturer_str:<25} | {f'{avg_rssi:.1f} dBm':<12} | {dist_str:<15}", end="\r")

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
    parser.add_argument("-r", "--rssi-history-size", type=int, default=20)
    parser.add_argument("-g", "--gamma", type=float, default = 2.5)
    
    args = parser.parse_args()

    target_mac = args.mac
    target_name = args.name
    rssi_history_size = args.rssi_history_size
    if rssi_history_size is None or rssi_history_size < 1 or rssi_history_size > 1000:
        rssi_history_size = 20
    n = args.gamma
    if n is None or n < 2 or n > 4:
        n = 2.5


    if not target_mac and not target_name:
        print("No device chosen. Scanning all BLE devices for 6 seconds ...")
        asyncio.run(scan_all_devices(n))
        exit(0)

    asyncio.run(track_device(
        target_mac=target_mac, 
        target_name=target_name, 
        rssi_history_size=rssi_history_size, 
        n=n))
