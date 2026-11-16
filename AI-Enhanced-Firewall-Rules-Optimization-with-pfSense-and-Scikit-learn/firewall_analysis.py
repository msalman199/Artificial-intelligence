import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load traffic data
df = pd.read_csv("traffic.csv", names=["frame_number", "src_ip", "dst_ip", "port", "size"])

# Feature engineering (e.g., frequency of traffic per source)
df['src_ip_count'] = df.groupby('src_ip')['src_ip'].transform('count')

# Select features for clustering
features = df[['src_ip_count', 'size']].values
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Apply KMeans clustering to identify traffic patterns
kmeans = KMeans(n_clusters=3, random_state=42)
df['traffic_cluster'] = kmeans.fit_predict(features_scaled)

# Visualize the traffic clusters
plt.scatter(df['src_ip_count'], df['size'], c=df['traffic_cluster'], cmap='viridis')
plt.xlabel('Source IP Frequency')
plt.ylabel('Packet Size')
plt.title('Traffic Clusters Based on Source IP and Packet Size')
plt.show()

# Display the most frequent source IPs with large packets
high_traffic = df[(df['traffic_cluster'] == 2) & (df['size'] > 500)]
print(high_traffic[['src_ip', 'size']])
