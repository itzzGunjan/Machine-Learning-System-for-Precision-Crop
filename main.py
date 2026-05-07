import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

app = FastAPI(title="Smart Farming API")

# --- Load Models & Encoders ---
try:
    with open("models/crop_model.pkl", "rb") as f:
        crop_model = pickle.load(f)
    with open("models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
        
    with open("models/fertilizer_model.pkl", "rb") as f:
        fertilizer_model = pickle.load(f)
    with open("models/fertilizer_scaler.pkl", "rb") as f:
        fertilizer_scaler = pickle.load(f)
    with open("models/soil_encoder.pkl", "rb") as f:
        soil_encoder = pickle.load(f)
    with open("models/crop_encoder.pkl", "rb") as f:
        crop_encoder = pickle.load(f)
except FileNotFoundError as e:
    print(f"Error loading models: {e}. Please run train_model.py first.")

# --- Pydantic Models ---
class CropRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

class FertilizerRequest(BaseModel):
    temperature: int
    humidity: int
    moisture: int
    soil_type: str
    crop_type: str
    N: int
    P: int
    K: int

# --- API Endpoints ---
@app.post("/api/predict-crop")
def predict_crop(data: CropRequest):
    try:
        # Prepare input array
        features = np.array([[
            data.N, data.P, data.K, 
            data.temperature, data.humidity, 
            data.ph, data.rainfall
        ]])
        
        # Scale features
        scaled_features = scaler.transform(features)
        
        # Predict
        prediction = crop_model.predict(scaled_features)[0]
        
        # Get confidence (probability of the predicted class)
        probabilities = crop_model.predict_proba(scaled_features)[0]
        confidence = float(np.max(probabilities))
        
        return {
            "crop": prediction,
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict-fertilizer")
def predict_fertilizer(data: FertilizerRequest):
    try:
        # Encode categorical features
        # Handle cases where input might not be in training set (though UI restricts to knowns)
        try:
            soil_encoded = soil_encoder.transform([data.soil_type])[0]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Unknown soil type: {data.soil_type}")
            
        try:
            crop_encoded = crop_encoder.transform([data.crop_type])[0]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Unknown crop type: {data.crop_type}")
            
        # Prepare input array
        features = np.array([[
            data.temperature, data.humidity, data.moisture,
            soil_encoded, crop_encoded,
            data.N, data.P, data.K
        ]])
        
        # Scale features
        scaled_features = fertilizer_scaler.transform(features)
        
        # Predict
        prediction = fertilizer_model.predict(scaled_features)[0]
        
        return {
            "fertilizer": prediction
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files to serve the frontend
# Serve index.html as the default for root "/"
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
