from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import time
import numpy as np
from scipy.optimize import minimize

app = FastAPI(title="BLE Trilateration Central Server")

# Storing of latest values from each scanner.
# { scanner_id: { device_identifier: data}}
active_readings: Dict[str, Dict[str, Any]] = {}

class DeviceTelemetry(BaseModel):
    scanner_id: str
    device_name: str
    mac: str
    avg_rssi: float
    distance: str
    x: float
    y: float

@app.post("/update")
async def receive_telemetry(data: DeviceTelemetry):
    timestamp = time.time()

    if data.scanner_id not in active_readings:
        active_readings[data.scanner_id] = {}

    if not data.device_name or data.device_name == "Unknown":
        return {"status": "ignored_unknown"}

    #key = data.mac if data.mac else data.device_name
    key = data.device_name.strip().lower()

    active_readings[data.scanner_id][key] = {
        "device_name": data.device_name,
        "mac": data.mac,
        "avg_rssi": data.avg_rssi,
        "distance": data.distance,
        "pos": (data.x, data.y),
        "timestamp": timestamp
    }

    print(f"[{data.scanner_id}] Tracked {data.device_name} ({data.mac}) -> RSSI: {data.avg_rssi:.1f} dBm, Dist: {data.distance}")
    return {"status": "ok"}

@app.get("/status")
async def get_status():
    return active_readings

@app.get("/position/{device_key}")
async def calculate_position(device_key: str):
    key = device_key.strip().lower()
    measurements = []

    for scanner_id, devices in active_readings.items():
        if key in devices:
            dev_data = devices[key]
            try:
                dist = float(dev_data["distance"].replace("~", "").replace(" meters", "").strip())
                rssi = dev_data["avg_rssi"]
                x, y = dev_data["pos"]
                measurements.append({
                    "scanner_id": scanner_id,
                    "pos": (x,y),
                    "dist": dist,
                    "rssi": rssi
                    })
            except ValueError:
                continue

    if len(measurements) < 2:
        return {"error": "Need data from at least 2 scanners to calculate position."}

    
    def error_function(coord):
        x, y = coord
        err = 0
        for m in measurements:
            sx, sy = m["pos"]
            d = m["dist"]
            calculated_dist = np.sqrt((x - sx)**2 + (y -sy)**2)
            err += (calculated_dist - d)**2
        return err

    strongest_scanner = max(measurements, key=lambda m: m["rssi"])
    initial_guess = strongest_scanner["pos"]

    result = minimize(error_function, initial_guess, method='Nelder-Mead')

    return {
            "device": device_key,
            "estimated_x": round(result.x[0], 2),
            "estimated_y": round(result.x[1], 2),
            "used_scanners": len(measurements),
            "primary_anchor": strongest_scanner["scanner_id"]
            }
