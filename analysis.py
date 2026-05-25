import pandas as pd

df = pd.read_excel("data/HIV_Adolescent_ART_Coverage_2025.xlsx", header=1)

print("Dataset loaded successfully")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())
for col in df.columns:
    print(f" - {col}")
