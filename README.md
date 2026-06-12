# 🛒 E-Commerce KPI Dashboard

An interactive ecommerce analytics dashboard built with Python, Streamlit, Pandas, and Plotly using the public `theLook Ecommerce` dataset from Google BigQuery.

---

# 📌 Project Overview

This project analyzes ecommerce business performance through key metrics such as:

* Revenue Growth
* Average Order Value (AOV)
* Customer Lifetime Value (LTV)
* Cohort Retention
* Customer Churn

The dashboard simulates a real-world analytics workflow:

* extracting raw data from BigQuery
* validating business data
* transforming metrics with Pandas
* building interactive dashboards for stakeholders

---

# 📥 Data Source

Dataset used:
`bigquery-public-data.thelook_ecommerce`

Source:
Google BigQuery Public Dataset

The raw tables were extracted into CSV files for local analysis and dashboard development.

Tables used:

* `orders`
* `order_items`
* `users`

---

# 📦 Data Extraction

Example extraction workflow using the BigQuery Python client:

```python id="3nml3g"
from google.cloud import bigquery

client = bigquery.Client()

query = """
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.orders`
"""

df = client.query(query).to_dataframe()

df.to_csv("orders.csv", index=False)
```

---

# 📊 Dashboard Pages

## 1. Overview Dashboard

High-level ecommerce business summary including:

* GMV trend
* LTV distribution
* Customer churn breakdown
* Revenue growth KPIs

---

## 2. Revenue Analytics

Tracks revenue performance over time:

* Gross Merchandise Value (GMV)
* Average Order Value (AOV)
* MoM Growth
* YoY Growth
* YTD Revenue

Interactive filtering supports dynamic metric exploration.

---

## 3. Customer Lifetime Value (LTV)

Customer segmentation analysis including:

* Average LTV
* Median LTV
* Top customer segments
* Tier classification (Bronze → Platinum)

---

## 4. Cohort Retention Analysis

Monthly cohort retention analysis using:

* Retention heatmaps
* Month-1 retention trends
* Customer return behavior

---

## 5. Customer Churn Analysis

Customer inactivity and churn monitoring:

* Active / At-Risk / Churned segmentation
* Revenue at risk
* Days since last order distribution
* High-value churned customers

---

# 🧹 Data Validation Approach

Since the dataset originates from Google BigQuery public warehouse tables, the project focuses primarily on data validation rather than extensive data cleaning.

Validation includes:

* duplicate checks
* null value checks
* datatype validation
* business rule filtering
* KPI sanity checks

Examples:

* excluding cancelled and returned orders
* validating retention rates
* validating revenue metrics

---

# 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* Plotly
* Google BigQuery

---

# 📂 Project Structure

```bash id="81r7rw"
project/
│
├── components/
│   ├── churn_charts.py
│   ├── churn_sidebar.py
│   ├── ltv_charts.py
│   ├── ltv_sidebar.py
│   ├── metric_cards.py
│   ├── overview_charts.py
│   ├── retention_charts.py
│   ├── retention_sidebar.py
│   ├── revenue_charts.py
│   └── revenue_sidebar.py
│
├── data/
│   ├── churn_df.py
│   ├── ltv_df.py
│   ├── retention_df.py
│   └── revenue_df.py
│
├── pages/
│   ├── overview.py
│   ├── revenue.py
│   ├── customer_ltv.py
│   ├── retention.py
│   └── churn.py
│
├── databases/
│   ├── orders.csv
│   ├── order_items.csv
│   └── users.csv
│
├── styles/
│   └── stylesheet.css
│
├── main_dashboard.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 📈 Key Business Metrics

| Metric         | Description                          |
| -------------- | ------------------------------------ |
| GMV            | Gross Merchandise Value              |
| AOV            | Average revenue per order            |
| LTV            | Total revenue generated per customer |
| Retention Rate | Percentage of returning customers    |
| Churn Rate     | Percentage of inactive customers     |

---

# 📋 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

streamlit
pandas
numpy
plotly
google-cloud-bigquery
db-dtypes
pyarrow

---

# 🚀 How to Run Locally

## 1. Clone Repository

```bash
git clone https://github.com/your-username/ecommerce-kpi-dashboard.git
cd ecommerce-kpi-dashboard
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Run Streamlit App

```bash
streamlit run main_dashboard.py
```

---

# ☁️ Deployment

This dashboard can be deployed easily using Streamlit Community Cloud.

Deployment steps:

1. Push project to GitHub
2. Login to Streamlit Cloud
3. Connect GitHub repository
4. Select `main_dashboard.py`
5. Deploy application

Streamlit Cloud:
https://share.streamlit.io

---

# 🎯 Project Goals

This project was built to practice:

* ecommerce analytics
* KPI development
* cohort analysis
* customer segmentation
* dashboard engineering
* business-focused data analysis

---

# 👨‍💻 Author

Arland
