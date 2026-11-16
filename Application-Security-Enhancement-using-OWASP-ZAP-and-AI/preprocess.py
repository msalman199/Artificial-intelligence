import json
import os
import pandas as pd

if os.path.exists("zap_results.json") and os.path.getsize("zap_results.json") > 0:
    with open("zap_results.json", "r") as f:
        alerts = json.load(f).get("alerts", [])
else:
    alerts = []

if len(alerts) >= 5:
    raw_df = pd.DataFrame(alerts)
    df = raw_df.groupby(["alert", "risk"]).agg(
        affected_url=("url", "first"),
        occurrences=("alert", "count")
    ).reset_index()
    df.rename(columns={"alert": "vulnerability_type", "risk": "severity"}, inplace=True)
else:
    print("Using sample dataset (fewer than 5 real alerts found in zap_results.json)...")
    data = {
        "vulnerability_type": [
            "SQL Injection", "XSS", "SQL Injection", "Broken Auth", "XSS",
            "Directory Traversal", "CSRF", "Information Disclosure", "SQL Injection", "XSS"
        ],
        "severity": ["High", "Medium", "High", "Low", "Medium", "High", "Medium", "Low", "High", "Medium"],
        "affected_url": [f"http://example.com{i}" for i in range(1, 11)],
        "occurrences": [10, 5, 8, 1, 6, 9, 4, 2, 12, 7]
    }
    df = pd.DataFrame(data)

severity_map = {"Informational": 0, "Low": 0, "Medium": 1, "High": 2, "Critical": 2}
df["severity_encoded"] = df["severity"].map(severity_map).fillna(0).astype(int)

df.to_csv("zap_vulnerabilities.csv", index=False)
print("Saved zap_vulnerabilities.csv:")
print(df.head())
