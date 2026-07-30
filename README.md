# 📊 State-wise GST Revenue Analysis in India

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Visualization-3F4F75?logo=plotly)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)

## 📌 Project Overview

This project analyzes **Goods and Services Tax (GST)** collection data across Indian States and Union Territories using Python. It demonstrates a complete data analytics workflow—from data cleaning and preprocessing to exploratory data analysis (EDA), statistical analysis, visualization, growth analysis, seasonality detection, anomaly detection, and interactive dashboard development.

The objective is to transform raw GST collection data into actionable insights that support data-driven decision-making for policymakers, analysts, and researchers.

---

## 🎯 Business Problem

GST collection data contains valuable information about economic activity across India. However, raw datasets alone do not provide insights into:

- Regional revenue contribution
- Revenue growth trends
- Monthly and yearly performance
- Tax component analysis
- Seasonal fluctuations
- Revenue anomalies

This project addresses these challenges using Python-based analytics and visualization techniques.

---

## 🚀 Project Objectives

- Analyze GST collections across Indian States and Union Territories
- Compare revenue contribution by region
- Study annual and monthly revenue trends
- Analyze CGST, SGST, IGST, and CESS contribution
- Calculate Year-over-Year (YoY) Growth
- Calculate Month-over-Month (MoM) Growth
- Detect seasonal patterns
- Identify revenue anomalies using IQR
- Build an interactive Streamlit dashboard

---

## 📂 Dataset Information

| Feature | Details |
|----------|----------|
| Dataset | Tax Collection on GST Portal |
| File Type | CSV |
| Records | 3,570 |
| Final Features | 12 |
| Coverage | Indian States & Union Territories |

**Dataset Source**

https://raw.githubusercontent.com/DurkadeviGanesanMCA/State-wise-GST-Revenue-Analysis-in-India-Using-Python/main/tax-collection-on-gst-portal.csv

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Google Colab
- GitHub
- Markdown

---

## 🔄 Project Workflow

```text
Data Collection
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Exploratory Data Analysis
      │
      ▼
Statistical Analysis
      │
      ▼
Visualization
      │
      ▼
Growth Analysis
      │
      ▼
Seasonality Analysis
      │
      ▼
Anomaly Detection
      │
      ▼
Business Insights
      │
      ▼
Interactive Dashboard
```

---

## 🧹 Data Preprocessing

The following preprocessing steps were performed:

- Missing value validation
- Duplicate record check
- Column renaming
- Date conversion
- Feature engineering
- Year extraction
- Month extraction
- Month-Year creation
- Region classification
- Total GST calculation

## Derived Features

- Total_GST
- Year
- Month
- Month_Year
- Month_Number
- Region_Type
- YoY_Growth_%
- MoM_Growth_%
- Anomaly

---

## 📊 Exploratory Data Analysis

The project includes:

- Dataset overview
- Data type validation
- Missing value analysis
- Duplicate analysis
- Descriptive statistics
- State-wise analysis
- Time-series analysis
- Distribution analysis

---
## 📊 Statistical Analysis Metrics

The project evaluates the statistical distribution of GST collections using the following descriptive metrics:

| 📈 Metric | 📋 Value | 💡 Interpretation |
|-----------|----------|-------------------|
| **Mean** | **₹2,628.00 Cr** | Average GST collection across all records. The higher mean compared to the median indicates the presence of high-value revenue observations. |
| **Median** | **₹1,003.99 Cr** | Represents the middle GST collection value and is less affected by extreme values than the mean. |
| **Mode** | **₹0.00 Cr** | The most frequently occurring value is zero, indicating many records with zero values for one or more GST components. |
| **Skewness** | **Positive (CGST: 3.23 – CESS: 18.01)** | All GST components exhibit strong positive skewness, meaning most observations are relatively low while a small number are exceptionally high. |
| **Kurtosis** | **High (Total GST: 29.07, CESS: 465.88)** | High kurtosis indicates heavy-tailed distributions and the presence of significant outliers, especially in the CESS component. |

## 📌 Key Statistical Insights

- 📊 **Mean > Median** for all GST components, indicating a **positively skewed distribution**.
- 📈 **Positive Skewness** suggests that a small number of states contribute disproportionately large GST revenues.
- 🚨 **High Kurtosis** confirms the presence of extreme observations and outliers, particularly in **CESS** collections.
- 📉 **Mode = 0** reflects frequent zero-value observations within the dataset.
- 📋 These statistical measures provide a comprehensive understanding of the **central tendency**, **distribution**, and **variability** of GST collections, supporting more informed exploratory analysis and business decision-making.
---

## 📉 Visualizations

The project includes interactive and static visualizations such as:

- Yearly GST Collection Trend
- Monthly GST Collection Trend
- State-wise GST Revenue
- Top 10 Revenue-Contributing States
- Bottom 5 Revenue-Contributing States
- GST Component Distribution
- YoY Growth Analysis
- MoM Growth Analysis
- Seasonal Analysis
- Boxplots
- Histograms
- Anomaly Detection Charts

---

## 📊 Insights for Project Objectives

## 1. Compare GST Collections Across Indian States and Union Territories

<img width="497" height="182" alt="image" src="https://github.com/user-attachments/assets/421a4df7-18e4-4091-84cf-a3eb76f8ed7d" />

## 🔍 Insight
- GST revenue is highly concentrated in a few economically developed states.
- **Maharashtra** recorded the highest cumulative GST collection (~₹19.14 lakh crore), followed by **Karnataka, Gujarat, Tamil Nadu, and Uttar Pradesh**.
- Smaller Union Territories such as **Lakshadweep, Ladakh, Andaman & Nicobar Islands, and Mizoram** contributed the least, reflecting their comparatively smaller economic activity.

---

## 2. Analyze GST Collection Trends by Month and Year

<img width="848" height="301" alt="image" src="https://github.com/user-attachments/assets/1997c33e-9a56-4e9b-a894-2fed326ee445" />

<img width="497" height="171" alt="image" src="https://github.com/user-attachments/assets/b037a7c2-1c68-42f4-9832-ba63d9d029bb" />


## 🔍 Insight
- Annual GST collections showed consistent growth from **2017–2019**, followed by a decline in **2020**, reflecting COVID-19-related economic disruption.
- Collections recovered strongly from **2021 onwards**, indicating improving economic activity.
- Monthly collections displayed recurring fluctuations, suggesting seasonality in GST payments.

---

## 3. Identify the Contribution of CGST, SGST, IGST and CESS

<img width="497" height="203" alt="image" src="https://github.com/user-attachments/assets/bbf4d882-ead1-405f-bb62-46f55264c523" />

## 🔍 Insight
- **IGST** contributed the largest share of total GST revenue, highlighting the importance of interstate trade and imports.
- **SGST** was the second-largest contributor, indicating strong intra-state commercial activity.
- **CGST** closely followed SGST, while **CESS** represented the smallest portion but remained important for compensation to states.

---

## 4. Determine the Highest and Lowest Revenue-Contributing Regions

<img width="497" height="283" alt="image" src="https://github.com/user-attachments/assets/72183d02-e841-40c6-8eb7-1ea7d7ab5819" />

<img width="497" height="301" alt="image" src="https://github.com/user-attachments/assets/bacf30c7-56f9-4805-99cb-9833a485df01" />


## 🔍 Insight

## 🏆 Top Contributors
| Rank | State |
|------|--------|
| 1 | Maharashtra |
| 2 | Karnataka |
| 3 | Gujarat |
| 4 | Tamil Nadu |
| 5 | Uttar Pradesh |

These states benefit from strong industrialization, manufacturing, services, IT, and trade sectors.

## 📉 Lowest Contributors

| Rank | State / UT |
|------|------------|
| 1 | Lakshadweep |
| 2 | Ladakh |
| 3 | Mizoram |
| 4 | Andaman & Nicobar Islands |
| 5 | Nagaland |

Lower collections correspond to smaller populations and comparatively lower levels of economic activity.

---

## 5. Calculate Year-over-Year (YoY) Growth

<img width="371" height="229" alt="image" src="https://github.com/user-attachments/assets/5a51191f-0659-41d6-82c6-9623e9a42a7e" />


## 🔍 Insight
- GST collections experienced exceptional growth in **2018** due to the GST implementation base effect.
- Revenue declined by **9.32% in 2020**, corresponding to the COVID-19 period.
- Positive growth resumed from **2021 through 2024**, indicating sustained economic recovery.
- Declines in **2025–2026** should be interpreted cautiously because the documentation notes possible incomplete data.

---

## 6. Calculate Month-over-Month (MoM) Growth

<img width="497" height="182" alt="image" src="https://github.com/user-attachments/assets/c405dee3-7a92-4f9c-8e19-08bb6f76e834" />

## 🔍 Insight
- Monthly GST growth showed considerable volatility.
- Growth ranged approximately from **−24.41% to 68.29%** (excluding the initial base-effect period).
- These fluctuations likely reflect tax payment schedules, fiscal cycles, seasonal demand, and economic activity.

---

## 7. Identify Seasonal Patterns in GST Revenue

<img width="497" height="184" alt="image" src="https://github.com/user-attachments/assets/b887bc79-0ddf-440b-9050-0ea4704dee60" />

## 🔍 Insight
- Seasonal analysis revealed recurring monthly variations in GST collections.
- Revenue patterns appear influenced by:
  - 🎉 Festival seasons
  - 📅 Fiscal year-end business activity
  - 🛒 Consumer spending cycles
  - 🧾 GST filing and payment schedules
- These recurring trends can support future forecasting and resource planning.

---

## 8. Detect Unusually High or Low GST Collection Periods

<img width="497" height="188" alt="image" src="https://github.com/user-attachments/assets/f398ea21-cb18-40f8-ab9e-b0f5c71bf23f" />

## 🔍 Insight
- The **Interquartile Range (IQR)** method successfully identified unusually high and low monthly GST collections.
- Detected anomalies may indicate:
  - Exceptional economic events
  - Large one-time tax collections
  - Policy changes
  - Compliance improvements
  - Data quality issues
- Each anomaly should be validated before drawing conclusions.

---

## 📌 Overall Project Insights

- 📈 Maharashtra remained the dominant contributor to India's GST collections.
- 📊 GST revenue recovered strongly after the COVID-19 slowdown.
- 🌐 IGST accounted for the largest share of total GST revenue.
- 📉 Revenue distribution was highly positively skewed, with a small number of regions contributing disproportionately large collections.
- 📅 Monthly and seasonal patterns suggest predictable cycles that can aid planning and forecasting.
- 🚨 IQR-based anomaly detection identified periods requiring further investigation.
- 🚀 The project establishes a scalable analytical framework for future forecasting, dashboarding, and policy support.

## 📊 Streamlit Dashboard

Interactive dashboard:

**https://state-wise-gst-revenue-analysis-in-india-using-python-ddfwyazy.streamlit.app/**

Dashboard Features:

- Interactive filters
- State-wise comparison
- Trend analysis
- Revenue breakdown
- Growth analysis
- Visual dashboards

---

## 📌 Business Recommendations

- Improve data quality validation.
- Monitor high-contribution states.
- Investigate anomalous revenue periods.
- Leverage seasonal trends for planning.
- Validate data completeness before forecasting.
- Automate monthly reporting pipelines.
- Expand predictive analytics using machine learning.

---

## 🔮 Future Enhancements

- Time-series forecasting
- Machine Learning models
- Automated ETL pipelines
- Real-time dashboard updates
- Economic indicator integration
- State-specific forecasting
- Automated anomaly alerts
- Role-based reporting

---
## 📦 Requirements

```text
pandas
numpy
matplotlib
seaborn
plotly
streamlit

---

## 👨‍💻 Author

**Durkdevi G**

Data Analyst | Python | SQL | Power BI | Excel | Streamlit



---

# ⭐ If you found this project useful, consider giving it a Star!
