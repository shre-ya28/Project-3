# 🏦 Customer Segmentation & Churn Pattern Analytics in European Banking

Segmentation-driven churn analytics for a European retail bank (France, Spain,
Germany) — built for **Unified Mentor / The European Central Bank** project brief.

Customer churn is one of the largest hidden costs in retail banking. This project
moves beyond a single aggregate churn rate to answer the questions that actually
drive retention strategy: *which* customer segments are most likely to churn, *how*
churn differs across countries and demographics, and *whether* churn is concentrated
among the bank's most valuable customers.

## 📊 Key Results

| KPI | Value |
|---|---|
| Overall Churn Rate | **20.37%** |
| High-Value Customer Churn Ratio | **25.08%** |
| Highest-Risk Market | Germany |
| Highest-Risk Age Band | 46–60 |
| Highest-Risk Product Count | 3–4 products held |
| Activity Effect | Inactive members churn at ~2x the rate of active members |

Full findings, methodology, and recommendations are in
[`reports/research_paper.md`](reports/research_paper.md) /
[`reports/Research_Paper.pdf`](reports/Research_Paper.pdf), with a stakeholder-facing
version in [`reports/Executive_Summary.docx`](reports/Executive_Summary.docx).

## 🗂️ Project Structure

```
bank_churn_project/
├── data/
│   └── European_Bank.csv          # Raw dataset (10,000 customers)
├── src/
│   ├── data_processing.py         # Load, validate, clean, and segment the data
│   └── kpi.py                     # Reusable KPI calculation functions
├── notebooks/
│   └── EDA_and_Churn_Analysis.ipynb   # Full exploratory data analysis
├── app/
│   └── streamlit_app.py           # Interactive churn analytics dashboard
├── images/                        # Exported chart images used in the research paper
├── reports/
│   ├── research_paper.md          # Full research paper (Markdown, GitHub-rendered)
│   ├── Research_Paper.pdf         # Same paper, PDF export
│   └── Executive_Summary.docx     # Executive summary for stakeholders
├── requirements.txt
└── README.md
```

## 🧩 Dataset

| Column | Description |
|---|---|
| CustomerId | Unique customer identifier |
| Surname | Customer surname (dropped during cleaning) |
| CreditScore | Customer creditworthiness |
| Geography | France, Spain, Germany |
| Gender | Male / Female |
| Age | Customer age |
| Tenure | Years with the bank |
| Balance | Account balance |
| NumOfProducts | Number of bank products held |
| HasCrCard | Credit card ownership |
| IsActiveMember | Activity indicator |
| EstimatedSalary | Estimated annual salary |
| Exited | Churn indicator (target) |

## 🧠 Segmentation Dimensions

The pipeline (`src/data_processing.py`) derives the following segments used
throughout the analysis and dashboard:

- **Geography:** France, Spain, Germany
- **Age Group:** <30, 30–45, 46–60, 60+
- **Credit Score Band:** Low (≤580), Medium (581–700), High (701+)
- **Tenure Group:** New (0–2 yrs), Mid-term (3–6 yrs), Long-term (7+ yrs)
- **Balance Segment:** Zero-balance, Low-balance, High-balance
- **Customer Value:** High-Value vs. Standard (balance & salary both ≥ median)
- **Engagement Level:** High / Medium / Low, from activity status + product count

## 🚀 Getting Started

### 1. Clone and set up the environment

```bash
git clone https://github.com/<your-username>/bank-churn-analytics.git
cd bank-churn-analytics
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Explore the analysis

```bash
jupyter notebook notebooks/EDA_and_Churn_Analysis.ipynb
```

### 3. Run the Streamlit dashboard

```bash
streamlit run app/streamlit_app.py
```

The dashboard opens at `http://localhost:8501` with four modules:

- **📊 Overall Summary** — headline churn KPIs, gender, credit score, and product-count breakdowns
- **🌍 Geography Explorer** — country-level churn rate, risk index, and a geography × age heatmap
- **👥 Age & Tenure** — age group, tenure group, engagement, and balance segment comparisons
- **💎 High-Value Customers** — high-value churn ratio, revenue-at-risk KPIs, and a churned high-value customer list

All four modules respond live to the sidebar segment filters (geography, gender, age
group, tenure group, balance segment, customer value, activity status).

## 🔑 KPIs Implemented

| KPI | Description | Where |
|---|---|---|
| Overall Churn Rate | % of customers who exited | `kpi.overall_churn_rate` |
| Segment Churn Rate | Churn % by any segment | `kpi.segment_churn_rate` |
| High-Value Churn Ratio | Churn among premium customers | `kpi.high_value_churn_ratio` |
| Geographic Risk Index | Regional churn exposure (rate × customer share) | `kpi.geographic_risk_index` |
| Engagement Drop Indicator | Inactivity vs. churn | `kpi.engagement_drop_indicator` |
| Revenue at Risk | Deposit balance / salary exposure tied to churned customers | `kpi.revenue_at_risk` |

## 📦 Deliverables

- ✅ Research paper — EDA, insights, and recommendations (`reports/research_paper.md`, `reports/Research_Paper.pdf`)
- ✅ Streamlit dashboard — live analytics (`app/streamlit_app.py`)
- ✅ Executive summary for stakeholders (`reports/Executive_Summary.docx`)

## 🛠️ Tech Stack

`Python` · `pandas` · `numpy` · `matplotlib` / `seaborn` (static EDA charts) ·
`plotly` (interactive dashboard charts) · `streamlit` · `Jupyter`

## 📄 License

This project is provided for educational and portfolio purposes as part of the
Unified Mentor program.
