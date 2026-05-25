# Nigeria HIV ART Coverage Dashboard

A polished Streamlit dashboard for exploring adolescent and young people HIV ART coverage data, with a focus on Nigeria and benchmark comparisons across countries.

## Overview

This project turns the workbook in `data/HIV_Adolescent_ART_Coverage_2025.xlsx` into an interactive public health dashboard that highlights:

- **Nigeria’s ART coverage** against the selected benchmark
- **Age-group comparisons** for Nigeria vs the global average
- **A global ranking chart** with Nigeria highlighted
- **Top 10 countries** table for the selected filters
- **Sidebar controls** for indicator, age group, sex, year, and UNICEF region

## Features

- Interactive **filters** for:
  - `Indicator`
  - `Age group`
  - `Sex`
  - `Year`
  - `UNICEF region`
- **Age-group comparison chart**
- **Ranking chart** with Nigeria highlighted
- **Top 10 countries** table
- Clean **portfolio-ready layout** with dashboard cards and a polished sidebar
- Data cleaning for values such as `4,100`, `>95`, and `<200`

## Project files

- `app.py` — main Streamlit dashboard
- `requirements.txt` — Python dependencies
- `hiv_analysis.py` — exploratory analysis script
- `data/` — input workbook used by the dashboard

## Installation

1. Create and activate a virtual environment
2. Install dependencies

```bash
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

## Data source

The dashboard uses the workbook in `data/HIV_Adolescent_ART_Coverage_2025.xlsx`.

## Technologies used

- `Streamlit` for the web dashboard
- `Pandas` for data loading and transformation
- `Altair` for interactive visualizations
- `OpenPyXL` for reading the workbook

## How it works

1. The workbook is loaded from `data/`.
2. The `Value` field is normalized so strings such as `4,100`, `>95`, and `<200` are safely converted to numeric values.
3. The sidebar filters are applied to build the ranking, comparison, and top-10 views.
4. The app renders polished metrics, charts, and a country table in a wide-layout dashboard.

## Deployment

This project can be hosted on:

- **Streamlit Cloud** for quick public deployment
- **Render** or **Railway** for a lightweight hosted app

## Project goals

- Provide a clean, decision-ready view of ART coverage performance
- Highlight Nigeria’s position relative to peers
- Offer a public-facing dashboard suitable for GitHub and portfolio sharing

## Notes

- The dashboard is designed for **public health reporting and portfolio presentation**.
- The `Value` field is cleaned before visualization so numeric formatting inconsistencies in the workbook do not break the app.

## Screenshots

Add your dashboard screenshots here once they are captured.

### Dashboard overview

![Dashboard overview](https://via.placeholder.com/1200x700?text=Dashboard+Overview)

### Ranking view

![Ranking view](https://via.placeholder.com/1200x700?text=Ranking+View)

### Top 10 countries table

![Top 10 countries table](https://via.placeholder.com/1200x700?text=Top+10+Countries)

## Future improvements

- Add a short narrative summary for each filter selection
- Include downloadable CSV or chart exports
- Add a reusable KPI section for key public health insights
