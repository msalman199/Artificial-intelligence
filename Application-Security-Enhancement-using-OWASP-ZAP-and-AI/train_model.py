import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load structured dataset
df = pd.read_csv("zap_vulnerabilities.csv")

X = df[["vulnerability_type", "occurrences"]]
y = df["severity_encoded"]

# Preprocess text categories + numeric features together
preprocessor = ColumnTransformer(
    transformers=[
        ("vuln", OneHotEncoder(handle_unknown="ignore"), ["vulnerability_type"]),
        ("num", "passthrough", ["occurrences"])
    ]
)

model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model_pipeline.fit(X_train, y_train)

y_pred = model_pipeline.predict(X_test)
print("Model Evaluation Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Save trained pipeline for live predictions
joblib.dump(model_pipeline, "zap_rf_model.pkl")
print("Model saved to zap_rf_model.pkl")
