 Smart Farming System

A Machine Learning-based web application that provides data-driven crop and fertilizer recommendations to farmers. By analyzing soil metrics and environmental conditions, this system eliminates guesswork and helps maximize agricultural yield.

##  Features

*   **Crop Recommendation:** Predicts the most optimal crop to plant based on Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, pH, and Rainfall.
*   **Fertilizer Prediction:** Recommends the exact fertilizer required by taking into account the soil metrics and the specific target crop.

##  Machine Learning Models

*   **Algorithm:** K-Nearest Neighbors (KNN) is used for both models due to its excellent performance with clustered agricultural data.
*   **Data Pre-processing:** Inputs are scaled and normalized using Scikit-Learn's `MinMaxScaler`.
*   **Performance:**
    *   Crop Recommendation Accuracy: **97.5%**
    *   Fertilizer Prediction Accuracy: **95.8%**

##  Tech Stack

*   **Backend:** Python, FastAPI
*   **Frontend:** HTML, CSS, JavaScript (served statically via FastAPI)
*   **Machine Learning:** Scikit-Learn, Pandas, NumPy

##  How to Run Locally

### 1. Prerequisites
Make sure you have Python installed on your machine.

### 2. Setup
Clone the repository and navigate into the project directory:
```bash
git clone https://github.com/itzzGunjan/Machine-Learning-System-for-Precision-Crop.git
cd Machine-Learning-System-for-Precision-Crop
```

### 3. Activate Virtual Environment
Activate the pre-existing virtual environment:
*   **Windows:**
    ```bash
    venv\Scripts\activate
    ```
*   **Mac/Linux:**
    ```bash
    source venv/bin/activate
    ```

### 4. Start the Server
Run the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload
```

### 5. Access the Web App
Open your web browser and go to:
👉 `http://127.0.0.1:8000`
