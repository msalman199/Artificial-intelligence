import re
import pandas as pd
import spacy
import matplotlib.pyplot as plt

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Sample dataset (Replace with df = pd.read_csv("your_data.csv") if loading from a file)
data = {
    "Name": ["John Doe", "Jane Smith"],
    "Email": ["john@example.com", "jane@test.org"],
    "Phone": ["555-123-4567", "555-987-6543"],
    "Address": ["123 Main St, New York", "456 Oak Ave, London"]
}
df = pd.DataFrame(data)

# Function to extract entities from text
def extract_entities(text):
    doc = nlp(str(text))
    entities = {}
    for ent in doc.ents:
        entities[ent.text] = ent.label_
    return entities

# Apply the function to the columns in the dataframe
personal_data = {}

for index, row in df.iterrows():
    name_entities = extract_entities(row["Name"])
    email_entities = extract_entities(row["Email"])
    phone_entities = extract_entities(row["Phone"])
    address_entities = extract_entities(row["Address"])

    personal_data[index] = {
        "Name_Entities": name_entities,
        "Email_Entities": email_entities,
        "Phone_Entities": phone_entities,
        "Address_Entities": address_entities
    }

# Display the extracted entities
for key, value in personal_data.items():
    print(f"Row {key}:")
    for field, entities in value.items():
        print(f"  {field}: {entities}")  # Fixed missing closing parenthesis

personal_data_tags = []

for index, row in df.iterrows():
    data_tags = []
    name_entities = extract_entities(row["Name"])
    address_entities = extract_entities(row["Address"])
    
    # Tagging logic for GDPR compliance
    if "PERSON" in name_entities.values():
        data_tags.append("Name")
    if re.search(r"[^@]+@[^@]+\.[^@]+", str(row["Email"])):
        data_tags.append("Email")
    if re.search(r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}", str(row["Phone"])):
        data_tags.append("Phone")
    if any(label in address_entities.values() for label in ["GPE", "LOC", "FAC"]) or len(str(row["Address"])) > 5:
        data_tags.append("Address")
    
    personal_data_tags.append(data_tags)

# Add tags to dataframe
df["GDPR_Tags"] = personal_data_tags
print("\nTagged DataFrame:")
print(df)

# Generate compliance report
compliance_report = []
for index, row in df.iterrows():
    report = {
        "Name": row["Name"],
        "Email": row["Email"],
        "Phone": row["Phone"],
        "Address": row["Address"],
        "GDPR_Tags": ", ".join(row["GDPR_Tags"]),
    }
    compliance_report.append(report)

compliance_df = pd.DataFrame(compliance_report)
compliance_df.to_csv("compliance_report.csv", index=False)
print("\nCompliance report generated: compliance_report.csv")

# Create a count of GDPR Tags
tag_counts = df["GDPR_Tags"].explode().value_counts()

# Plot and save the distribution of tags
if not tag_counts.empty:
    tag_counts.plot(kind='bar', color='skyblue')
    plt.title("GDPR Data Distribution")
    plt.xlabel("Data Type")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("gdpr_distribution.png")
    print("Chart saved to: gdpr_distribution.png")

