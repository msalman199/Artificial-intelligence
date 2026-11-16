import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Load Snort alert data (replace with your own log file)
data = []
with open('snort_alerts.txt', 'r') as file:
    for line in file:
        # Extract relevant fields (example: IP addresses, ports, alert type)
        parts = line.split()
        src_ip = parts[1]
        dst_ip = parts[3]
        alert_type = parts[-1]  # last part is alert type

        data.append([src_ip, dst_ip, alert_type])

# Create DataFrame
df = pd.DataFrame(data, columns=["src_ip", "dst_ip", "alert_type"])

# Encode alert type (0: normal, 1: intrusion)
le = LabelEncoder()
df["alert_label"] = le.fit_transform(df["alert_type"])

# Feature extraction (e.g., length of src_ip, dst_ip)
df["src_ip_len"] = df["src_ip"].apply(lambda x: len(x))
df["dst_ip_len"] = df["dst_ip"].apply(lambda x: len(x))

# Example: create more features based on the logs
# df["some_feature"] = some_feature_extraction_function(df)

print(df.head())
