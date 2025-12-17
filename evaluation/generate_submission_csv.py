import csv
import requests

# ===== CONFIG =====
API_URL = "http://127.0.0.1:8000/recommend"  # change to deployed URL later
TOP_K = 5

# Test queries (use UNLABELED test queries provided by SHL)
queries = [
    "Need a Java developer who can collaborate with business teams",
    "Looking for a data analyst with SQL and Python skills",
    "Hiring for an analyst role using cognitive and personality tests"
]

output_file = "evaluation/submission.csv"

# ===== CSV GENERATION =====
with open(output_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Query", "Assessment_url"])  # HEADER (EXACT)

    for query in queries:
        response = requests.post(
            API_URL,
            json={"job_description": query, "top_k": TOP_K}
        )
        response.raise_for_status()

        results = response.json()["recommended_assessments"]

        for r in results:
            writer.writerow([query, r["url"]])

print(f"CSV generated successfully: {output_file}")
