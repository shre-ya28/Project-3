# Customer Segmentation & Churn Pattern Analytics in European Banking

**Prepared for:** The European Central Bank (via Unified Mentor)
**Analysis type:** Exploratory Data Analysis, Segmentation Design, Churn Pattern Analytics
**Dataset:** 10,000 retail banking customers across France, Spain, and Germany

---

## Abstract

Customer churn is one of the largest hidden costs in retail banking, driving down
lifetime value, raising acquisition costs, and destabilizing revenue. This paper
presents a segmentation-driven analysis of a 10,000-customer dataset from a European
retail bank operating in France, Spain, and Germany. We validate and clean the data,
construct five segmentation dimensions (geography, age, credit score, tenure, and
balance), and quantify churn behavior across each. We find an overall churn rate of
**20.37%**, with pronounced concentration among customers aged 46–60, customers
holding three or more products, inactive members, and — critically — high-value
customers, who churn at a higher rate (25.1%) than the customer base as a whole. We
close with segment-specific retention recommendations.

---

## 1. Background and Context

Banks routinely track an aggregate churn rate, but an aggregate number cannot answer
the questions that matter operationally: *which* customers are leaving, *where*, and
*why*. Without granular segmentation, retention strategies default to blanket,
reactive campaigns that spend budget on customers who were never going to leave while
missing the segments driving most of the loss. This project addresses that gap by
building a structured, segmentation-driven analytics layer on top of customer-level
banking data.

## 2. Problem Statement

Despite having rich customer-level records, the bank faces three concrete challenges:

1. Identifying which customer segments carry disproportionate churn risk.
2. Understanding how churn differs across the three countries and across demographic
   groups within them.
3. Quantifying the financial exposure — deposit balances and income — tied to the
   customers who actually leave.

## 3. Dataset Description

The dataset contains 10,000 customer records with the following fields: `CustomerId`,
`Surname` (dropped — not analytical), `CreditScore`, `Geography` (France, Spain,
Germany), `Gender`, `Age`, `Tenure` (years with the bank), `Balance`, `NumOfProducts`,
`HasCrCard`, `IsActiveMember`, `EstimatedSalary`, and the binary target `Exited`. The
data contained no missing values, and all binary fields (`HasCrCard`,
`IsActiveMember`, `Exited`) were confirmed to contain only 0/1 values during
validation.

**Class balance:** 79.63% retained vs. 20.37% churned — a moderate imbalance that is
accounted for by reporting rates and shares rather than raw counts throughout this
analysis.

## 4. Methodology

### 4.1 Data Ingestion & Validation
The raw CSV was loaded and checked for null values, valid category labels
(`Geography`, `Gender`), and binary-field consistency before any analysis began.

### 4.2 Data Cleaning & Preparation
The non-analytical `Surname` field was removed, and the data was checked for
duplicate `CustomerId` records (none were found).

### 4.3 Segmentation Design
Five segmentation dimensions were engineered from the raw fields:

| Dimension | Bands |
|---|---|
| Geography | France, Spain, Germany |
| Age | <30, 30–45, 46–60, 60+ |
| Credit Score | Low (≤580), Medium (581–700), High (701+) |
| Tenure | New (0–2 yrs), Mid-term (3–6 yrs), Long-term (7+ yrs) |
| Balance | Zero-balance, Low-balance (<€100k), High-balance (≥€100k) |

A **High-Value** flag was additionally derived for customers whose balance *and*
estimated salary are both at or above the dataset median, and an **Engagement Level**
field combining activity status and product count.

---

## 5. Churn Distribution Analysis

### 5.1 Overall Churn Rate

![Overall churn distribution](../images/01_overall_churn.png)

The bank's overall churn rate is **20.37%** — roughly one in every five customers
exited during the period covered by the data.

### 5.2 Churn by Geography

![Churn by geography](../images/02_churn_by_geography.png)

Germany shows the highest churn rate of the three markets, despite hosting roughly
half as many customers as France. Spain has the lowest churn rate. Because France
carries by far the largest customer base, it also contributes the largest *absolute*
number of churned customers even though its *rate* is lower than Germany's — a
distinction that matters for how retention budget should be allocated (rate vs.
volume).

### 5.3 Churn by Age Group

![Churn by age group](../images/03_churn_by_age.png)

Churn rises sharply for customers in the 46–60 age band relative to customers under
45, then eases somewhat for the 60+ group. This mid-to-late-career segment appears to
be the bank's highest-risk age cohort.

### 5.4 Churn by Credit Score Band

![Churn by credit score](../images/07_churn_by_creditscore.png)

Churn rate is relatively stable across credit score bands, suggesting creditworthiness
alone is a weak predictor of churn in this population — segmentation by behavioral and
engagement variables is more informative than by credit standing.

### 5.5 Churn by Tenure Group

![Churn by tenure](../images/08_churn_by_tenure.png)

Tenure shows a comparatively flat relationship with churn; long-standing customers are
not meaningfully more "locked in" than newer ones, which argues against assuming
loyalty accrues automatically over time.

### 5.6 Churn by Balance Segment

![Churn by balance segment](../images/06_churn_by_balance.png)

Customers holding a non-zero balance churn at a different rate than zero-balance
customers, indicating that dormant/zero-balance accounts and actively-funded accounts
require distinct retention treatments.

---

## 6. Comparative Demographic Analysis

### 6.1 Gender-Based Churn Differences

![Churn by gender](../images/04_churn_by_gender.png)

Female customers churn at a modestly higher rate than male customers in this dataset.

### 6.2 Geography × Age Interaction

![Geography x age heatmap](../images/05_geo_age_heatmap.png)

The heatmap reveals that the elevated churn seen in the 46–60 age band is not evenly
distributed across countries — it is markedly more pronounced in Germany than in
France or Spain, pointing to a specific, targetable segment: **German customers aged
46–60**.

### 6.3 Financial Stability vs. Churn

![Churn by number of products](../images/09_churn_by_numproducts.png)

The relationship between product count and churn is the single strongest pattern in
this dataset: customers holding **3 or 4 products churn at a dramatically higher rate**
than those holding 1–2 products, even though the 3–4 product group is a small share of
the base. Counter-intuitively, more product cross-sell does not equal more loyalty in
this population — it may instead signal customers who were sold products that did not
fit their needs, or who are already disengaging and being over-marketed to as a result.

![Churn by activity](../images/10_churn_by_activity.png)

Inactive members churn at roughly double the rate of active members, confirming
activity status as a strong, low-cost early-warning signal that the bank can monitor
continuously.

---

## 7. High-Value Customer Churn Analysis

![Churn by customer value](../images/11_churn_by_highvalue.png)

Customers classified as **High-Value** (balance and salary both at or above the median)
churn at **25.08%**, noticeably above the base rate of 20.37%. This is the analysis's
most consequential finding: **the bank is losing its most profitable customers at a
higher rate than its average customer**, which has an outsized effect on lifetime
value and revenue stability relative to the headline churn figure.

![Balance distribution churned vs retained](../images/12_balance_distribution.png)

The balance distribution of churned customers is shifted toward higher balances
relative to retained customers, reinforcing that churn is not concentrated among
low-balance, low-engagement accounts alone.

**Revenue exposure:** across the full customer base, churned customers collectively
held a substantial share of total deposit balances and estimated income, a concrete
euro-denominated stand-in for the annual revenue at risk from churn (see the live
figures in the Streamlit dashboard's High-Value Customer Explorer tab, which updates
with any segment filter applied).

---

## 8. Correlation Analysis

![Correlation matrix](../images/13_correlation_matrix.png)

`Age`, `NumOfProducts`, and `IsActiveMember` show the strongest linear association
with `Exited` among the numerical features, consistent with the segment-level findings
above. `EstimatedSalary`, `HasCrCard`, and `Tenure` show weak linear association with
churn individually — their value in this analysis comes from segment *interactions*
(e.g., high salary combined with high balance) rather than as standalone predictors.

---

## 9. Key Performance Indicators — Summary Table

| KPI | Value |
|---|---|
| Overall Churn Rate | 20.37% |
| High-Value Churn Ratio | 25.08% |
| Highest-Risk Geography | Germany |
| Highest-Risk Age Band | 46–60 |
| Highest-Risk Product Count | 3–4 products |
| Active vs. Inactive Churn Gap | Inactive members churn at ~2x the rate of active members |

*(Exact figures for any filtered segment are available live in the Streamlit
dashboard.)*

---

## 10. Recommendations

1. **Prioritize Germany, and specifically German customers aged 46–60**, for a
   dedicated retention campaign — this is the highest-concentration risk pocket
   identified in the geography × age interaction.
2. **Investigate the 3–4 product segment as a churn signal, not just a cross-sell
   success.** Route customers who cross a product-count threshold into a proactive
   relationship-management check-in rather than further product marketing.
3. **Treat inactivity as an early-warning trigger.** Build an automated alert when a
   customer's activity status flips to inactive, and pair it with a low-cost
   re-engagement outreach before churn risk compounds.
4. **Build a distinct high-value retention track.** Because high-value customers churn
   at an above-average rate, assign them to relationship managers or premium retention
   offers rather than the same generic campaigns used for the broader base.
5. **De-prioritize credit score and tenure as standalone targeting variables** — the
   data does not support them as strong differentiators of churn risk on their own.

---

## 11. Conclusion

This segmentation-driven analysis moves the bank from a single aggregate churn number
to an actionable map of where churn risk concentrates: **Germany, mid-career
customers, multi-product holders, inactive members, and — most importantly for
revenue — high-value customers.** The accompanying Streamlit dashboard operationalizes
these findings into a live, filterable tool so that retention, marketing, and
relationship-management teams can monitor and act on these segments continuously
rather than relying on static, retrospective reporting.
