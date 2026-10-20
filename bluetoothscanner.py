import asyncio
import math
from bleak import BleakScanner

# Databas med kända Bluetooth-tillverkare (Company IDs)
COMPANY_IDS = {
    0x004C: "Apple Inc.",
    0x0075: "Samsung Electronics",
    0x0006: "Microsoft",
    0x00E0: "Google LLC",
    0x02D0: "Sony Corporation",
    0x0059: "Nordic Semiconductor (IoT/Smarta prylar)",
    0x000A: "Qualcomm Technologies",
    0x000D: "Texas Instruments",
    0x01DA: "Logitech",
    0x0087: "Garmin",
    0x01B5: "Bose Corporation",
    0x0057: "Harman International (JBL)",
    0x02E5: "Espressif Systems (ESP32 / Smart hem)",
    0x07D7: "Tuya Smart (Smart hem-enheter)",
    0x038F: "Xiaomi Inc.",
    0x003C: "Broadcom",
    0x000F: "Broadcom",
    0x005D: "Realtek Semiconductor",
    0x001D: "Qualcomm / Atheros",
    0x0180: "Huawei Technologies",
    0x0001: "Nokia Mobile Phones",
    0x0399: "Anker Innovations (Soundcore)",
    0x012D: "Sennheiser",
}

def estimate_distance(rssi, tx_power):
    """Beräknar avstånd inomhus (Log-distance path loss)."""
    if rssi is None or rssi == 0:
        return "Okänt"
    
    if tx_power is None or tx_power == 0 or tx_power > 10 or tx_power < -100:
        tx_power = -59

    n = 2.5
    try:
        dist = 10 ** ((tx_power - rssi) / (10 * n))
        return round(dist, 1)
    except OverflowError:
        return "> 50.0"

def parse_apple_data(raw_bytes):
    """Avkodar Apples dolda sändningsformat och avläser AirPods-batteri."""
    if len(raw_bytes) < 2:
        return "Okänd Apple-data"
    
    type_byte = raw_bytes[0]
    hex_str = raw_bytes.hex()
    
    if type_byte == 0x07:
        # AirPods Proximity Pairing (Typ 0x07)
        if len(raw_bytes) >= 14:
            # 1. Kolla om batteriet skickas som rena procentbytes (0x64 = 100%)
            b_left_raw = raw_bytes[11] if len(raw_bytes) > 11 else 0xFF
            b_right_raw = raw_bytes[12] if len(raw_bytes) > 12 else 0xFF
            b_case_raw = raw_bytes[13] if len(raw_bytes) > 13 else 0xFF

            def parse_single_battery(val):
                if val == 0xFF or val == 0x0F:
                    return "Ej aktiv / I etui"
                if val <= 100:
                    return f"{val}%"
                # Om det skickas som 0-10 skala (nibble)
                low_nibble = val & 0x0F
                if low_nibble <= 10:
                    return f"{low_nibble * 10}%"
                return "Ej aktiv"

            # Om 0x64 (100%) eller liknande finns i sekvensen
            if b_left_raw <= 100 or b_right_raw <= 100:
                left_str = parse_single_battery(b_left_raw)
                right_str = parse_single_battery(b_right_raw)
                case_str = parse_single_battery(b_case_raw)
            else:
                # 2. Alternativ avkodning via nibbles (Apple Proximity v2)
                # Byte 6 och 7 innehåller ofta nibbles för Left/Right/Case (0-10)
                b_status1 = raw_bytes[6] if len(raw_bytes) > 6 else 0xFF
                b_status2 = raw_bytes[7] if len(raw_bytes) > 7 else 0xFF
                
                left_nib = (b_status1 >> 4) & 0x0F
                right_nib = b_status1 & 0x0F
                case_nib = (b_status2 >> 4) & 0x0F

                left_str = f"{left_nib * 10}%" if left_nib <= 10 else "Ej aktiv"
                right_str = f"{right_nib * 10}%" if right_nib <= 10 else "Ej aktiv"
                case_str = f"{case_nib * 10}%" if case_nib <= 10 else "Ej aktiv"

            return (f"AirPods Status:\n"
                    f"       • Vänster snäcka: {left_str}\n"
                    f"       • Höger snäcka:   {right_str}\n"
                    f"       • Laddningsetui:  {case_str}")
        else:
            return f"Apple AirPods Proximity State (Söker anslutning, Hex: {hex_str[4:16]}...)"
            
    elif type_byte == 0x12:
        return "Apple Handoff / AirPlay Status"
    elif type_byte == 0x10:
        return "Apple Nearby Action / AirTag / Find My Network"
    elif type_byte == 0x0F:
        return "Apple HomeKit / Smart Hem"
    elif type_byte == 0x09:
        return "Apple AirDrop"
    elif type_byte == 0x13:
        return "Apple Nearby Info / Find My Status"
    else:
        return f"Apple-specifik kod (Typ: 0x{type_byte:02x})"

async def main():
    print("Skannar efter BLE-enheter i 6 sekunder...")
    
    devices_data = await BleakScanner.discover(timeout=6.0, return_adv=True)
    
    parsed_devices = []

    for device, adv in devices_data.values():
        name = device.name or adv.local_name or "Ej namngiven"
        
        m_list = []
        raw_m_data = {}
        apple_info = ""

        if adv.manufacturer_data:
            for comp_id, raw_bytes in adv.manufacturer_data.items():
                comp_name = COMPANY_IDS.get(comp_id, f"Okänd (ID: 0x{comp_id:04x})")
                m_list.append(comp_name)
                raw_m_data[f"0x{comp_id:04x}"] = raw_bytes.hex()

                if comp_id == 0x004C:
                    apple_info = parse_apple_data(raw_bytes)

        m_str = ", ".join(m_list) if m_list else "Ingen tillverkardata"
        tx_pwr = adv.tx_power
        dist = estimate_distance(adv.rssi, tx_pwr)
        
        # Poängberäkning för integritetsanalys
        info_score = 0
        if name != "Ej namngiven": 
            info_score += 5
        if m_list and "Okänd" not in m_list[0]: 
            info_score += 2
        if adv.service_uuids: 
            info_score += 2
        if tx_pwr is not None: 
            info_score += 1
        if apple_info: 
            info_score += 3
        if adv.rssi > -60: 
            info_score += 2

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
            "info_score": info_score
        })

    # SORTERING: Längst bort först -> Närmast längst ner
    parsed_devices.sort(key=lambda x: x["rssi"], reverse=False)

    print("\n" + "="*70)
    print(" SKANNINGSRESULTAT (LÄNGST BORT FÖRST -> NÄRMAST LÄNGST NER)")
    print("="*70 + "\n")

    for d in parsed_devices:
        print(f"  MAC/UUID:      {d['address']}")
        print(f"  Namn:          {d['name']}")
        print(f"  Signalstyrka:  {d['rssi']} dBm  (Uppskattat avstånd: ~{d['distance']} m)")
        print(f"  Tillverkare:   {d['manufacturer']}")
        
        if d['apple_info']:
            print(f"  Apple Status:  {d['apple_info']}")
        if d['tx_power'] is not None:
            print(f"  TX Power:      {d['tx_power']} dBm")
        if d['uuids']:
            print(f"  Tjänster:      {d['uuids']}")
        if d['raw_m_data']:
            print(f"  Rådata (Hex):  {d['raw_m_data']}")
            
        print("-" * 60)

    # SAMMANFATTNING
    total_found = len(parsed_devices)
    named_count = sum(1 for d in parsed_devices if d['name'] != "Ej namngiven")
    top_informative = sorted(parsed_devices, key=lambda x: x["info_score"], reverse=True)[:3]

    print("\n" + "="*70)
    print(" SAMMANFATTNING OCH INTEGRITETSANALYS")
    print("="*70)
    print(f"Totalt antal hittade enheter: {total_found}")
    print(f"Enheter som avslöjade sitt namn: {named_count} av {total_found}")
    print(f"Enheter nära dig (RSSI > -70 dBm): {sum(1 for d in parsed_devices if d['rssi'] > -70)}")
    print("\n" + "-"*70)
    print(" TOP 3 ENHETER SOM LÄCKER MEST INFORMATION")
    print("-" * 70 + "\n")

    for i, dev in enumerate(top_informative, 1):
        if dev['info_score'] > 0:
            print(f"  Plats {i}: {dev['name']}")
            print(f"  MAC/UUID:     {dev['address']}")
            print(f"  Tillverkare:  {dev['manufacturer']}")
            if dev['apple_info']:
                print(f"  Detaljer:     {dev['apple_info']}")
            print(f"  Tjänster:     {len(dev['uuids'])} st identifierade")
            print(f"  Signalstyrka: {dev['rssi']} dBm (~{dev['distance']} m)")
            print("\n")

asyncio.run(main())