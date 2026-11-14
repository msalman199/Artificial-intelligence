import pandas as pd
import numpy as np

# Simulate risk data: Asset value, threat event frequency, vulnerability, and impact
np.random.seed(42)

data = {
    "asset_value": np.random.uniform(1000, 5000, 100),  # Value in dollars
    "threat_event_frequency": np.random.uniform(0.1, 1.0, 100),  # Frequency (per year)
    "vulnerability": np.random.uniform(0.1, 1.0, 100),  # Probability of a successful attack
    "impact": np.random.uniform(100, 1000, 100),  # Impact value (in dollars)
    "historical_loss": np.random.uniform(500, 3000, 100)  # Historical loss as an outcome
}

df = pd.DataFrame(data)
print(df.head())
