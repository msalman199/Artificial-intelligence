import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# Simulated system metrics (CPU, Memory usage)
np.random.seed(42)
data = {
    "cpu_usage": np.random.normal(50, 5, 1000),  # Normal CPU usage (50%)
    "memory_usage": np.random.normal(60, 10, 1000)  # Normal memory usage (60%)
}
# Simulate anomalies (outliers)
data["cpu_usage"][200:250] = np.random.normal(90, 5, 50)  # High CPU usage anomaly
data["memory_usage"][400:450] = np.random.normal(20, 5, 50)  # Low memory usage anomaly

df = pd.DataFrame(data)

# Train an anomaly detection model (Isolation Forest)
model = IsolationForest(contamination=0.05)
model.fit(df)

# Save the trained model
joblib.dump(model, 'anomaly_detection_model.pkl')

# Predict anomalies
df["anomaly"] = model.predict(df)
df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})  # 1 for anomaly, 0 for normal
print(df.head())

