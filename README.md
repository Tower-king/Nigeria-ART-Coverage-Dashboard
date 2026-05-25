# Nigeria HIV ART Coverage Dashboard

A polished Streamlit dashboard for exploring adolescent and young people HIV ART coverage data, with a focus on Nigeria and benchmark comparisons across countries.

## Overview

This project turns the workbook in HIV_Adolescent_ART_Coverage_2025.xlsx into an interactive public health dashboard that highlights:

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

The dashboard uses the workbook in `HIV_Adolescent_ART_Coverage_2025.xlsx` sourced from UNAIDS public databank.

## Technologies used

- Streamlit for the web dashboard
- Pandas for data loading and transformation
- Altair for interactive visualizations
- OpenPyXL for reading the workbook
- Matplotlib for plotting graphs

## How it works

1. The sidebar filters are applied to build the ranking, comparison, and top-10 views.
2. The app renders polished metrics, charts, and a country table in a wide-layout dashboard.

## Deployment

This project can be hosted on:

- **Streamlit Cloud** for quick public deployment
- **Render** or **Railway** for a lightweight hosted app

## Project goals

- Provide a clean, decision-ready view of ART coverage performance
- Highlight Nigeria’s position relative to peers
- Offer a public-facing dashboard suitable for GitHub and portfolio sharing

### Dashboard overview
(https://github.com/Tower-king/Nigeria-ART-Coverage-Dashboard/blob/main/Dashboard.JPG)

### Ranking view

https://github.com/Tower-king/Nigeria-ART-Coverage-Dashboard/blob/main/ranking.JPG

### Top 10 countries table

https://github.com/Tower-king/Nigeria-ART-Coverage-Dashboard/blob/main/top%2010%20countries.JPG
