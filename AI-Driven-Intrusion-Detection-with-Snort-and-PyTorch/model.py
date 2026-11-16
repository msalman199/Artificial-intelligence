import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

np.random.seed(42)

normal_X = np.random.randint(7, 12, size=(100, 2))
normal_y = np.zeros(100, dtype=int)

intrusion_X = np.random.randint(13, 19, size=(100, 2))
intrusion_y = np.ones(100, dtype=int)

X_combined = np.vstack((normal_X, intrusion_X))
y_combined = np.concatenate((normal_y, intrusion_y))

df = pd.DataFrame({
    "src_ip_len": X_combined[:, 0],
    "dst_ip_len": X_combined[:, 1],
    "alert_label": y_combined
})

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

X = df[["src_ip_len", "dst_ip_len"]].values
y = df["alert_label"].values

X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.long)

dataset = TensorDataset(X_tensor, y_tensor)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

model = IntrusionDetectionModel()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 25
for epoch in range(num_epochs):
    for inputs, labels in dataloader:
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 5 == 0:
        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")

torch.save(model.state_dict(), "intrusion_model.pth")
print("Model saved successfully to intrusion_model.pth")
