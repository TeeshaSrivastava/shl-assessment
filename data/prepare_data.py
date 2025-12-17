import pandas as pd

# Load Excel dataset (REAL source)
df = pd.read_excel("Gen_AI Dataset.xlsx")

print("Columns found:", df.columns.tolist())

# Normalize URL column
if "Assessment_url" in df.columns:
    df["url"] = df["Assessment_url"]
elif "Assessment URL" in df.columns:
    df["url"] = df["Assessment URL"]
else:
    raise ValueError("No assessment URL column found")

# Generate name from URL
def infer_name(url):
    if isinstance(url, str) and url.strip():
        return url.rstrip("/").split("/")[-1].replace("-", " ").title()
    return "SHL Assessment"

df["name"] = df["url"].apply(infer_name)

# Default description and test type
df["description"] = "Assessment aligned to role requirements."
df["test_type"] = [[] for _ in range(len(df))]

# Save cleaned dataset
df[["name", "url", "description", "test_type"]].to_json(
    "data/assessments_clean.json", orient="records", indent=2
)

print(f"Saved {len(df)} assessments successfully")

      