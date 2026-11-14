import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("mem_free_data.csv")
df["time_idx"] = range(len(df))

X = df[["time_idx"]]
y = df["mem_free"]

model = LinearRegression()
model.fit(X, y)

future = pd.DataFrame({"time_idx": range(len(df), len(df)+20)})
future["mem_free_pred"] = model.predict(future)

plt.plot(df["time_idx"], y, label="Actual")
plt.plot(future["time_idx"], future["mem_free_pred"], label="Predicted", linestyle="--")
plt.xlabel("Time Index")
plt.ylabel("Memory Free (bytes)")
plt.title("Memory Forecast")
plt.legend()
plt.savefig("memory_forecast.png")
plt.show()
