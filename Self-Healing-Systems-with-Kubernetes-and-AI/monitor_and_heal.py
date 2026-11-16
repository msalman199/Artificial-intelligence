import joblib
import numpy as np
import pandas as pd
from kubernetes import client, config

# Load pre-trained anomaly detection model
model = joblib.load('anomaly_detection_model.pkl')

# Initialize Kubernetes client
config.load_kube_config()
v1 = client.CoreV1Api()

# Simulate pod metrics (matches the raw scale used in model.py)
cpu_usage = np.random.normal(50, 5)
memory_usage = np.random.normal(60, 10)
print(f"Current Metrics -> CPU: {cpu_usage:.2f}%, Memory: {memory_usage:.2f}%")

# Predict anomaly using a DataFrame with matching feature names
data = pd.DataFrame([[cpu_usage, memory_usage]], columns=["cpu_usage", "memory_usage"])
anomaly = model.predict(data)

if anomaly[0] == -1:
    print("Anomaly detected! Triggering self-healing process.")
    
    # Dynamically fetch running pods in the default namespace
    pods = v1.list_namespaced_pod(namespace="default")
    
    if pods.items:
        # Target the first pod found (or filter by label_selector="app=your-app")
        pod_name = pods.items[0].metadata.name
        v1.delete_namespaced_pod(name=pod_name, namespace="default")
        print(f"Pod {pod_name} deleted and being rescheduled.")
    else:
        print("No running pods found in the 'default' namespace to heal.")
else:
    print("System metrics are normal. No action needed.")

