import torch
import torch.nn as nn

# 1. Define the exact same model architecture used during training
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

# 2. Initialize the model and load the saved weights
model = IntrusionDetectionModel()
model.load_state_dict(torch.load("intrusion_model.pth", weights_only=True))

# 3. Simulate real-time prediction from Snort data
new_data = torch.tensor([[16, 15]], dtype=torch.float32)  # Example: incoming traffic features

# 4. Predict using the trained model
model.eval()
with torch.no_grad():
    prediction = model(new_data)

# 5. Check if prediction indicates an intrusion
predicted_label = prediction.argmax(dim=1).item()
if predicted_label == 1:
    print("Intrusion detected! Triggering response.")
    # Example: Block the offending IP or rescale the system
    # subprocess.run(["sudo", "ufw", "deny", "from", "192.168.1.50"])
else:
    print("Traffic is normal. No action needed.")
