# Predict future risk scenario
new_data = pd.DataFrame({
    "asset_value": [3000],
    "threat_event_frequency": [0.8],
    "vulnerability": [0.7],
    "impact": [500]
})

# Predict the loss for the new scenario
future_loss = model.predict(new_data)
print(f"Predicted risk (loss) for the new scenario: ${future_loss[0]:.2f}")
