import matplotlib.pyplot as plt

# Generate some new scenarios
new_scenarios = pd.DataFrame({
    "asset_value": np.random.uniform(1000, 5000, 50),
    "threat_event_frequency": np.random.uniform(0.1, 1.0, 50),
    "vulnerability": np.random.uniform(0.1, 1.0, 50),
    "impact": np.random.uniform(100, 1000, 50)
})

# Predict loss for all new scenarios
predicted_losses = model.predict(new_scenarios)

# Plot the results
plt.hist(predicted_losses, bins=10, color='skyblue', edgecolor='black')
plt.xlabel("Predicted Loss ($)")
plt.ylabel("Frequency")
plt.title("Distribution of Predicted Risk Losses")
plt.show()
