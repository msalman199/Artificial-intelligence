import os
import re
import time
import subprocess
import torch
import torch.nn as nn

# 1. Define the exact model architecture from model.py
class IntrusionDetectionModel(nn.Module):
    def __init__(self):
        super(IntrusionDetectionModel, self).__init__()
        self.fc1 = nn.Linear(2, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 2. Load trained PyTorch weights
model = IntrusionDetectionModel()
model.load_state_dict(torch.load("intrusion_model.pth", weights_only=True))
model.eval()

ALERT_LOG = "/var/log/snort/alert"
LOCAL_RULES = "/etc/snort/rules/local.rules"
blocked_ips = set()
current_sid = 2000001

# Regex to extract Source IP and Destination IP from Snort alert lines (e.g., 192.168.1.5:443 -> 172.31.10.210:80)
IP_PATTERN = re.compile(r"(\d+\.\d+\.\d+\.\d+)(?::\d+)?\s*->\s*(\d+\.\d+\.\d+\.\d+)(?::\d+)?")

def update_firewall_and_snort(src_ip):
    global current_sid
    if src_ip in blocked_ips or src_ip.startswith("127.") or src_ip.startswith("172.31."):
        return

    print(f"[AI ALERT] Intrusion predicted from {src_ip}. Executing self-healing actions...")

    # Action A: Block IP in UFW firewall
    subprocess.run(["sudo", "ufw", "deny", "from", src_ip], check=False)
    print(f"  -> Firewall updated: Blocked {src_ip} via UFW.")

    # Action B: Append a new rule to Snort local.rules
    new_rule = f'alert ip {src_ip} any -> $HOME_NET any (msg:"AI-Generated Rule: Blocked Malicious IP {src_ip}"; sid:{current_sid}; rev:1;)\n'
    current_sid += 1

    with open(LOCAL_RULES, "a") as rule_file:
        rule_file.write(new_rule)
    print(f"  -> Snort rules updated: Added SID {current_sid - 1} to {LOCAL_RULES}.")

    # Action C: Reload Snort daemon to apply the new rule
    subprocess.run(["sudo", "pkill", "-HUP", "snort"], check=False)
    print("  -> Snort reloaded with updated rules.\n")

    blocked_ips.add(src_ip)

def monitor_snort_logs():
    print(f"Monitoring {ALERT_LOG} in real time with AI model...")
    if not os.path.exists(ALERT_LOG):
        print(f"Waiting for {ALERT_LOG} to be created by Snort...")
        while not os.path.exists(ALERT_LOG):
            time.sleep(2)

    with open(ALERT_LOG, "r") as f:
        # Move pointer to the end of the file to read only new real-time alerts
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue

            match = IP_PATTERN.search(line)
            if match:
                src_ip, dst_ip = match.group(1), match.group(2)
                features = torch.tensor([[float(len(src_ip)), float(len(dst_ip))]], dtype=torch.float32)

                with torch.no_grad():
                    output = model(features)
                    predicted_label = output.argmax(dim=1).item()

                if predicted_label == 1:
                    update_firewall_and_snort(src_ip)
                else:
                    print(f"[NORMAL] Traffic {src_ip} -> {dst_ip} classified as benign.")

if __name__ == "__main__":
    monitor_snort_logs()
