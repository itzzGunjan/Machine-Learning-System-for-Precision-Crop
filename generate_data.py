import pandas as pd
import numpy as np
import random
import os

def generate_crop_data(num_samples=2200):
    crops = ['Rice', 'Maize', 'Chickpea', 'Kidneybeans', 'Pigeonpeas', 
             'Mothbeans', 'Mungbean', 'Blackgram', 'Lentil', 'Pomegranate', 
             'Banana', 'Mango', 'Grapes', 'Watermelon', 'Muskmelon', 
             'Apple', 'Orange', 'Papaya', 'Coconut', 'Cotton', 'Jute', 'Coffee']
    
    data = []
    samples_per_crop = num_samples // len(crops)
    
    for crop in crops:
        # Create somewhat distinct clusters for each crop so KNN works well
        base_n = random.randint(0, 100)
        base_p = random.randint(5, 120)
        base_k = random.randint(5, 180)
        base_temp = random.uniform(15.0, 35.0)
        base_hum = random.uniform(30.0, 95.0)
        base_ph = random.uniform(4.5, 8.5)
        base_rain = random.uniform(40.0, 250.0)
        
        for _ in range(samples_per_crop):
            # Add some variance
            n = max(0, min(140, base_n + random.randint(-10, 10)))
            p = max(5, min(145, base_p + random.randint(-10, 10)))
            k = max(5, min(205, base_k + random.randint(-10, 10)))
            temp = max(8.0, min(45.0, base_temp + random.uniform(-2, 2)))
            hum = max(14.0, min(100.0, base_hum + random.uniform(-5, 5)))
            ph = max(3.5, min(9.9, base_ph + random.uniform(-0.5, 0.5)))
            rain = max(20.0, min(298.0, base_rain + random.uniform(-10, 10)))
            
            data.append([n, p, k, round(temp, 2), round(hum, 2), round(ph, 2), round(rain, 2), crop])
            
    df = pd.DataFrame(data, columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/crop.csv', index=False)
    print(f"Generated crop.csv with {len(df)} records.")

def generate_fertilizer_data(num_samples=500):
    soil_types = ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey']
    crop_types = ['Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Barley', 'Wheat', 'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts']
    fertilizers = ['Urea', 'DAP', '14-35-14', '28-28', '20-20', '10-26-26']
    
    data = []
    
    for _ in range(num_samples):
        temp = random.randint(25, 38)
        hum = random.randint(50, 72)
        moisture = random.randint(25, 65)
        soil = random.choice(soil_types)
        crop = random.choice(crop_types)
        
        # Make the N, P, K correlate with the fertilizer
        fert = random.choice(fertilizers)
        if fert == 'Urea':
            n, p, k = random.randint(35, 42), random.randint(0, 10), random.randint(0, 10)
        elif fert == 'DAP':
            n, p, k = random.randint(15, 20), random.randint(35, 42), random.randint(0, 10)
        elif fert == '14-35-14':
            n, p, k = random.randint(10, 15), random.randint(30, 38), random.randint(10, 15)
        elif fert == '28-28':
            n, p, k = random.randint(25, 30), random.randint(25, 30), random.randint(0, 10)
        elif fert == '20-20':
            n, p, k = random.randint(18, 22), random.randint(18, 22), random.randint(0, 10)
        else: # 10-26-26
            n, p, k = random.randint(8, 12), random.randint(22, 28), random.randint(22, 28)
            
        data.append([temp, hum, moisture, soil, crop, n, p, k, fert])
        
    df = pd.DataFrame(data, columns=['temperature', 'humidity', 'moisture', 'soil_type', 'crop_type', 'N', 'P', 'K', 'fertilizer'])
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/fertilizer.csv', index=False)
    print(f"Generated fertilizer.csv with {len(df)} records.")

if __name__ == '__main__':
    generate_crop_data()
    generate_fertilizer_data()
