import joblib
import pandas as pd

# Load trained model
model = joblib.load("zap_rf_model.pkl")

# Simulate newly detected vulnerabilities from a fresh ZAP scan
new_vulnerabilities = pd.DataFrame({
    "vulnerability_type": ["SQL Injection", "Cross-Site Request Forgery", "Broken Authentication"],
    "occurrences": list((9, 4, 3)),
    "source_ip": ["203.0.113.45", "198.51.100.12", "192.0.2.88"]
})

# Predict severity (0 = Low, 1 = Medium, 2 = High)
predictions = model.predict(new_vulnerabilities[["vulnerability_type", "occurrences"]])
reverse_map = {0: "Low", 1: "Medium", 2: "High"}
new_vulnerabilities["predicted_severity"] = [reverse_map[p] for p in predictions]

print("AI Prediction Results:")
print(new_vulnerabilities[["vulnerability_type", "occurrences", "predicted_severity"]])
print("\n--- Automated Defensive Actions ---")

for _, row in new_vulnerabilities.iterrows():
    vuln = row["vulnerability_type"]
    sev = row["predicted_severity"]
    ip = row["source_ip"]

    if sev == "High":
        ufw_cmd = f"sudo ufw deny from {ip} to any"
        snort_rule = f'drop tcp {ip} any -> $HOME_NET any (msg:"AI-Blocked High Severity {vuln}"; sid:1000001; rev:1;)'
        print(f"[HIGH ALERT] {vuln} detected -> Triggering immediate mitigation:")
        print(f"   -> Firewall Action: {ufw_cmd}")
        print(f"   -> Snort Rule:      {snort_rule}")
    elif sev == "Medium":
        print(f"[MEDIUM] {vuln} detected -> Queued for patch review and rate-limiting.")
    else:
        print(f"[LOW] {vuln} detected -> Logged for routine maintenance.")
