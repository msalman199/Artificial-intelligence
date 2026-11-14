import pandas as pd
import mlflow
import os
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
mlflow.set_tracking_uri("file://" + os.path.abspath("mlruns"))
mlflow.set_experiment("CI_CD_Optimization")

df = pd.read_csv("build_times.csv", names=["timestamp", "duration"])

with mlflow.start_run():
    avg_time = df["duration"].mean()
    latest_time = df["duration"].iloc[-1]

    mlflow.log_metric("latest_build_time", latest_time)
    mlflow.log_metric("average_build_time", avg_time)
    print(f"Logged to MLflow: latest={latest_time}, average={avg_time}")
