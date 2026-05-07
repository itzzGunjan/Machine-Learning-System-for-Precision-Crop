import requests

print("Testing Crop API...")
res = requests.post("http://127.0.0.1:8000/api/predict-crop", json={
    "N": 90, "P": 42, "K": 43, 
    "temperature": 20.8, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9
})
print(res.json())

print("Testing Fertilizer API...")
res = requests.post("http://127.0.0.1:8000/api/predict-fertilizer", json={
    "temperature": 26, "humidity": 52, "moisture": 38,
    "soil_type": "Sandy", "crop_type": "Maize",
    "N": 37, "P": 0, "K": 0
})
print(res.json())
