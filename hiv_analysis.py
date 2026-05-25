# HIV/AIDS Data Analysis Project
# Step 1: Import libraries

import pandas as pd


def clean_numeric_value(value):
    if pd.isna(value):
        return None
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned == "":
            return None
        if cleaned.startswith(">") or cleaned.startswith("<"):
            cleaned = cleaned[1:]
        cleaned = cleaned.replace(",", "")
        if cleaned == "":
            return None
        return float(cleaned)
    return float(value)


data = pd.read_excel("data/HIV_Adolescent_ART_Coverage_2025.xlsx")

df = pd.read_excel("data/HIV_Adolescent_ART_Coverage_2025.xlsx", index_col=0)

df = pd.read_excel("data/HIV_Adolescent_ART_Coverage_2025.xlsx", header=1)

df["Value"] = df["Value"].apply(clean_numeric_value)

df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

nigeria = df[
    (df["Country/Region"] == "Nigeria") &
    (df["Indicator"] == "Per cent of adolescents and/or young people living with HIV receiving ART") &
    (df["Sex"] == "Both")
]

nigeria = df[
    (df["Country/Region"] == "Nigeria") &
    (df["Indicator"] == "Per cent of adolescents and/or young people living with HIV receiving ART")
]
import matplotlib.pyplot as plt

#bar chart
import matplotlib.pyplot as plt

coverage = df[
    (df["Indicator"] == "Per cent of adolescents and/or young people living with HIV receiving ART") &
    (df["Age"] == "Age 15-24") &
    (df["Sex"] == "Both")
].copy()

coverage["Value"] = coverage["Value"].apply(clean_numeric_value)
coverage["Value"] = pd.to_numeric(coverage["Value"], errors="coerce")

coverage = coverage.sort_values("Value", ascending=False)

coverage["Rank"] = range(1, len(coverage)+1)

nigeria = coverage[coverage["Country/Region"] == "Nigeria"]

print(nigeria[["Rank","Country/Region","Value"]])

summary = {
    "Metric": [
        "Nigeria ART Coverage (15-24)",
        "Nigeria Global Rank",
        "Female Coverage",
        "Male Coverage",
        "Coverage Age 15-19",
        "Coverage Age 15-24"
    ],
    "Value": [
        "77%",
        "43",
        "78%",
        "75%",
        "60%",
        "77%"
    ]
}

import pandas as pd

summary_df = pd.DataFrame(summary)

print(summary_df)

nigeria_rank = coverage[
    coverage["Country/Region"] == "Nigeria"
]["Rank"].iloc[0]

neighbors = coverage.iloc[
    max(0, nigeria_rank-3):
    min(len(coverage), nigeria_rank+2)
]

print(
    neighbors[
        ["Rank", "Country/Region", "Value"]
    ]
)

ranking = df[
    (df["Indicator"] == "Per cent of adolescents and/or young people living with HIV receiving ART") &
    (df["Age"] == "Age 15-24") &
    (df["Sex"] == "Both")
].copy()

ranking["Value"] = ranking["Value"].apply(clean_numeric_value)
ranking["Value"] = pd.to_numeric(ranking["Value"], errors="coerce")

ranking = ranking.sort_values("Value", ascending=False)

ranking["Rank"] = range(1, len(ranking) + 1)

print(ranking[["Rank", "Country/Region", "Value"]].head(20))

import matplotlib.pyplot as plt

countries = ["Nigeria", "Zambia", "Tanzania", "Botswana", "Eswatini"]

comparison = ranking[
    ranking["Country/Region"].isin(countries)
]

plt.figure(figsize=(8,5))

plt.bar(
    comparison["Country/Region"],
    comparison["Value"]
)

plt.title(
    "Nigeria vs Selected Countries: ART Coverage (15–24 Years)"
)

plt.ylabel("Coverage (%)")

plt.show()

import streamlit as st

st.set_page_config(
    page_title="Nigeria HIV/AIDS Data Analysis",
    page_icon="📊",
    layout="wide"
)
st.title("Nigeria HIV/AIDS ART Coverage Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("ART Coverage (15-24)", "77%")

with col2:
    st.metric("Global Rank", "43")

with col3:
    st.metric("Female Coverage", "78%")

st. markdown("---")

st.subheader("Key Findings")

st.write("""
- Nigeria ranked 43rd globally for ART coverage among adolescents and young people aged 15-24.
- ART coverage was 77%.
- Female coverage (78%) was slightly higher than male coverage (75%).
- Coverage among adolescents aged 15-19 was 60%
""")