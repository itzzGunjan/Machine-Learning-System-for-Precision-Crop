import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_crop_model():
    print("--- Training Crop Recommendation Model (KNN) ---")
    
    # 1. Load Data
    try:
        df = pd.read_csv('data/crop.csv')
    except FileNotFoundError:
        print("Error: data/crop.csv not found.")
        return

    # 2. Prepare Features and Label
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']

    # 3. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Feature Scaling (MinMaxScaler)
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 5. Train KNN Model
    # Use k=5 as default
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)

    # 6. Evaluate Accuracy
    y_pred = knn.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"Crop Model Accuracy: {acc * 100:.2f}%")

    # 7. Sample Prediction
    sample = X_test.iloc[[0]]
    sample_scaled = scaler.transform(sample)
    prediction = knn.predict(sample_scaled)[0]
    actual = y_test.iloc[0]
    print(f"Sample Prediction -> Predicted: {prediction}, Actual: {actual}")

    # 8. Save Model and Scaler
    os.makedirs('models', exist_ok=True)
    with open('models/crop_model.pkl', 'wb') as f:
        pickle.dump(knn, f)
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print("Saved crop_model.pkl and scaler.pkl to models/")
    print()


def train_fertilizer_model():
    print("--- Training Fertilizer Recommendation Model (Random Forest) ---")
    
    # 1. Load Data
    try:
        df = pd.read_csv('data/fertilizer.csv')
    except FileNotFoundError:
        print("Error: data/fertilizer.csv not found.")
        return

    # 2. Prepare Features and Label
    X = df[['temperature', 'humidity', 'moisture', 'soil_type', 'crop_type', 'N', 'P', 'K']]
    y = df['fertilizer']

    # 3. Label Encoding for Categorical Features
    soil_encoder = LabelEncoder()
    crop_encoder = LabelEncoder()
    
    X_encoded = X.copy()
    X_encoded['soil_type'] = soil_encoder.fit_transform(X['soil_type'])
    X_encoded['crop_type'] = crop_encoder.fit_transform(X['crop_type'])

    # 4. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # 4.5. Feature Scaling (MinMaxScaler) for KNN
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 5. Train KNN Model
    # Use n_neighbors to match the report's 95.8% accuracy, 5 is a good default
    knn_fert = KNeighborsClassifier(n_neighbors=5)
    knn_fert.fit(X_train_scaled, y_train)

    # 6. Evaluate Accuracy
    y_pred = knn_fert.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"Fertilizer Model Accuracy: {acc * 100:.2f}%")

    # 7. Sample Prediction
    sample = X_test.iloc[[0]]
    sample_scaled = scaler.transform(sample)
    prediction = knn_fert.predict(sample_scaled)[0]
    actual = y_test.iloc[0]
    print(f"\nSample Prediction -> Predicted: {prediction}, Actual: {actual}")

    # 8. Save Model and Encoders
    os.makedirs('models', exist_ok=True)
    with open('models/fertilizer_model.pkl', 'wb') as f:
        pickle.dump(knn_fert, f)
    with open('models/fertilizer_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open('models/soil_encoder.pkl', 'wb') as f:
        pickle.dump(soil_encoder, f)
    with open('models/crop_encoder.pkl', 'wb') as f:
        pickle.dump(crop_encoder, f)
    print("Saved fertilizer_model.pkl, fertilizer_scaler.pkl, soil_encoder.pkl, and crop_encoder.pkl to models/")
    print()

if __name__ == '__main__':
    train_crop_model()
    train_fertilizer_model()
