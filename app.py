import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

st.set_page_config(
    page_title="Nigeria HIV ART Coverage Dashboard",
    page_icon="🩺",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
    }
    .metric-card {
        border-radius: 18px;
        padding: 1rem 1rem 0.9rem 1rem;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.93), rgba(30, 41, 59, 0.88));
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
    }
    .metric-card h3 {
        margin-bottom: 0.25rem;
        color: #e2e8f0;
    }
    .metric-card p {
        margin-top: 0.25rem;
        color: #cbd5e1;
    }
    .dashboard-kicker {
        color: #38bdf8;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-size: 0.78rem;
    }
    .sidebar-note {
        font-size: 0.92rem;
        color: #cbd5e1;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

import os 
DATA_PATH = os.path.join(os.path.dirname(__file__), "HIV_Adolescent_ART_Coverage_2025.xlsx")


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH, header=1)

    def clean_value(value):
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

    df["Value"] = df["Value"].apply(clean_value)
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    return df


@st.cache_data(show_spinner=False)
def get_dashboard_data(indicator: str, age: str, sex: str, year: int, region: str):
    df = load_data()

    base_mask = (
        (df["Indicator"] == indicator)
        & (df["Age"] == age)
        & (df["Sex"] == sex)
        & (df["Year"] == year)
        & (df["Type"] == "Country")
    )
    if region != "All":
        base_mask &= df["UNICEF Region"] == region

    ranked = df.loc[base_mask].copy()
    ranked = ranked.dropna(subset=["Value"])
    ranked = ranked.sort_values(["Value", "Country/Region"], ascending=[False, True]).reset_index(drop=True)
    ranked["Rank"] = range(1, len(ranked) + 1)

    comparison = df.loc[
        (df["Indicator"] == indicator)
        & (df["Sex"] == sex)
        & (df["Year"] == year)
        & (df["Type"] == "Country")
        & (df["Country/Region"] == "Nigeria")
    ].copy()
    comparison = comparison.dropna(subset=["Value"])

    global_avg = (
        df.loc[
            (df["Indicator"] == indicator)
            & (df["Sex"] == sex)
            & (df["Year"] == year)
            & (df["Type"] == "Country")
        ]
        .groupby("Age", observed=True)["Value"]
        .mean()
        .reset_index(name="Global average")
    )

    return ranked, comparison, global_avg


def build_age_comparison_chart(comparison: pd.DataFrame, global_avg: pd.DataFrame):
    if comparison.empty:
        return (
            alt.Chart(pd.DataFrame({"Age": [], "Coverage": []}))
            .mark_bar()
            .encode(
                x=alt.X("Age:N", title="Age group"),
                y=alt.Y("Coverage:Q", title="Coverage (%)"),
            )
        )

    nigeria_series = comparison[["Age", "Value"]].copy()
    nigeria_series["Metric"] = "Nigeria"
    nigeria_series = nigeria_series.rename(columns={"Value": "Coverage"})

    global_series = global_avg[["Age", "Global average"]].copy()
    global_series["Metric"] = "Global average"
    global_series = global_series.rename(columns={"Global average": "Coverage"})

    chart_data = pd.concat([nigeria_series, global_series], ignore_index=True)
    age_order = sorted(chart_data["Age"].dropna().unique().tolist())
    chart_data["Age"] = pd.Categorical(chart_data["Age"], categories=age_order, ordered=True)
    chart_data = chart_data.sort_values(["Age", "Metric"])

    base = alt.Chart(chart_data).encode(
        x=alt.X("Age:N", title="Age group", sort=age_order),
        y=alt.Y("Coverage:Q", title="Coverage (%)", scale=alt.Scale(domain=[0, 100])),
        color=alt.Color(
            "Metric:N",
            scale=alt.Scale(range=["#f59e0b", "#38bdf8"]),
            title=None,
        ),
        tooltip=[
            alt.Tooltip("Age:N", title="Age group"),
            alt.Tooltip("Metric:N", title="Series"),
            alt.Tooltip("Coverage:Q", title="Coverage (%)", format=".0f"),
        ],
    )

    return base.mark_bar().properties(height=320)


def build_ranking_chart(ranked: pd.DataFrame):
    if ranked.empty:
        return (
            alt.Chart(pd.DataFrame({"Country/Region": [], "Value": []}))
            .mark_bar()
            .encode(
                x=alt.X("Value:Q", title="Coverage (%)"),
                y=alt.Y("Country/Region:N", title=None),
            )
        )

    chart_data = ranked.copy()
    chart_data["Highlight"] = chart_data["Country/Region"].eq("Nigeria")

    base = alt.Chart(chart_data).encode(
        x=alt.X("Value:Q", title="Coverage (%)", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y(
            "Country/Region:N",
            sort=chart_data.sort_values("Value", ascending=False)["Country/Region"].tolist(),
            title=None,
            axis=alt.Axis(labels=False),
        ),
        tooltip=[
            alt.Tooltip("Rank:Q", title="Rank"),
            alt.Tooltip("Country/Region:N", title="Country"),
            alt.Tooltip("Value:Q", title="Coverage (%)", format=".0f"),
            alt.Tooltip("UNICEF Region:N", title="UNICEF region"),
        ],
    )

    bars = base.mark_bar().encode(
        color=alt.condition(
            alt.datum.Highlight,
            alt.value("#f59e0b"),
            alt.value("#0f172a"),
        ),
        opacity=alt.condition(alt.datum.Highlight, alt.value(1.0), alt.value(0.76)),
    )

    return bars.properties(height=max(520, len(chart_data) * 12))


df = load_data()
indicator_options = sorted(df["Indicator"].dropna().unique().tolist())

st.sidebar.header("Dashboard filters")
st.sidebar.markdown(
    "<div class='sidebar-note'>Use the controls to compare ART coverage across years, age bands, sex, and UNICEF regions. Nigeria is highlighted in the ranking view.</div>",
    unsafe_allow_html=True,
)

indicator = st.sidebar.selectbox("Indicator", indicator_options, index=0)
age_options = sorted(df.loc[df["Indicator"] == indicator, "Age"].dropna().unique().tolist())
sex_options = sorted(df.loc[df["Indicator"] == indicator, "Sex"].dropna().unique().tolist())
year_options = sorted(df["Year"].dropna().unique().tolist())
region_options = ["All"] + sorted(df["UNICEF Region"].dropna().unique().tolist())

age = st.sidebar.selectbox("Age group", age_options, index=min(len(age_options) - 1, 1))
sex = st.sidebar.selectbox("Sex", sex_options, index=0)
year = st.sidebar.selectbox("Year", year_options, index=len(year_options) - 1)
region = st.sidebar.selectbox("UNICEF region", region_options)

ranked, comparison, global_avg = get_dashboard_data(indicator, age, sex, year, region)

nigeria_row = ranked[ranked["Country/Region"] == "Nigeria"]
coverage_value = nigeria_row["Value"].iloc[0] if not nigeria_row.empty else None
rank_value = nigeria_row["Rank"].iloc[0] if not nigeria_row.empty else None
country_count = int(ranked["Country/Region"].nunique()) if not ranked.empty else 0

st.markdown(
    """
    <div class='dashboard-kicker'>Public health dashboard</div>
    <h1 style='margin: 0.25rem 0 0.6rem 0;'>Nigeria HIV ART coverage and benchmarking dashboard</h1>
    <p style='max-width: 900px; color: #cbd5e1; margin-bottom: 1.2rem;'>
        Explore ART coverage performance across age groups and countries, with Nigeria highlighted for decision-ready public health analysis.
    </p>
    """,
    unsafe_allow_html=True,
)

st.sidebar.divider()
st.sidebar.subheader("Current snapshot")
st.sidebar.metric("Nigeria coverage", f"{coverage_value:.0f}%" if coverage_value is not None else "N/A")
st.sidebar.metric("Nigeria rank", int(rank_value) if rank_value is not None else "N/A")
st.sidebar.metric("Countries in view", country_count)

metric_cols = st.columns(3)
with metric_cols[0]:
    st.markdown(
        f"""
        <div class='metric-card'>
            <h3>Coverage</h3>
            <div style='font-size: 1.8rem; font-weight: 700; color: #f8fafc;'>""" + (f"{coverage_value:.0f}%" if coverage_value is not None else "N/A") + """</div>
            <p>Nigeria's selected ART coverage for the current filter set.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with metric_cols[1]:
    st.markdown(
        f"""
        <div class='metric-card'>
            <h3>Global rank</h3>
            <div style='font-size: 1.8rem; font-weight: 700; color: #f8fafc;'>""" + (str(int(rank_value)) if rank_value is not None else "N/A") + """</div>
            <p>Rank among countries using the selected age, sex, year, and region filters.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with metric_cols[2]:
    st.markdown(
        f"""
        <div class='metric-card'>
            <h3>Countries in view</h3>
            <div style='font-size: 1.8rem; font-weight: 700; color: #f8fafc;'>""" + str(country_count) + """</div>
            <p>The number of countries available after applying the current filters.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

left_col, right_col = st.columns([1.1, 1.1])

with left_col:
    st.subheader("Age-group comparison")
    st.caption("Nigeria is compared against the global average for the selected sex and year across the available age bands.")
    if comparison.empty:
        st.info("Nigeria does not have a value for the chosen age band in this dataset, so the chart shows the available age bands only.")
    st.altair_chart(build_age_comparison_chart(comparison, global_avg), use_container_width=True)

with right_col:
    st.subheader("Nigeria on the global ranking chart")
    st.caption("The chart is sorted by coverage and Nigeria is highlighted so its rank is easy to identify.")
    if ranked.empty:
        st.warning("No country-level data match the selected filters. Adjust the filters to view the ranking chart.")
    else:
        st.altair_chart(build_ranking_chart(ranked), use_container_width=True)

st.divider()

st.subheader("Top 10 countries")
if ranked.empty:
    st.warning("No country-level data are available for the selected filters.")
else:
    top10 = ranked.head(10)[["Rank", "Country/Region", "Value", "UNICEF Region"]].copy()
    top10["Value"] = top10["Value"].map(lambda x: f"{x:.0f}%" if pd.notna(x) else "N/A")
    st.dataframe(top10, use_container_width=True, hide_index=True)

st.caption(
    "Source: HIV adolescent ART coverage workbook. Values are cleaned for charting so comparisons remain robust even when the raw file contains bounded values such as >95."
)
