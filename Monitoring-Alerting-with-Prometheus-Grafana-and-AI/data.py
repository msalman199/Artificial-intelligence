import requests
import pandas as pd
import time

end = int(time.time())
start = end - 3600  # last 1 hour

url = f"http://localhost:9090/api/v1/query_range?query=node_memory_MemFree_bytes&start={start}&end={end}&step=15"
resp = requests.get(url).json()

values = resp['data']['result'][0]['values']
df = pd.DataFrame(values, columns=["timestamp", "mem_free"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
df["mem_free"] = df["mem_free"].astype(float)
df.to_csv("mem_free_data.csv", index=False)
