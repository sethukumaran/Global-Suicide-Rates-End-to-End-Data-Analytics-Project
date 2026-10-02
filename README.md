# Global-Suicide-Rates-End-to-End-Data-Analytics-Project

## 1. Project Overview

This project analyzes a global suicide-rate dataset containing country, year, sex, age group, suicide rate, GDP, GDP per capita, and population information.
The objective is to demonstrate an end-to-end **senior data analyst workflow**:
- Data quality assessment
- Exploratory data analysis (EDA)
- Trend analysis
- Demographic segmentation
- Country benchmarking
- Socioeconomic relationship analysis
- SQL-based business/policy questions
- Python visualization
- Action-oriented interpretation
- GitHub-ready project structure

> **Important analytical note:** Suicide is a sensitive public-health outcome. This project is intended for descriptive analytics and resource-planning discussion. The analysis does not establish causality, and country comparisons should account for differences in reporting, estimation methods, population structure, and local context.


## 2. Dataset Summary

| Attribute | Result |
|---|---:|
| Rows | 18,315 |
| Countries | 185 |
| Years | 2000–2021 |
| Sex categories | 3: both, male, female |
| Age categories | 12 |
| Main metric | Suicide rate per 100,000 |
| Economic metrics | GDP, GDP per capita |
| Population | Total country population |
| Duplicate rows | 0 |
| Missing GDP/GDP per capita rows | 315 |

The dataset contains 12,210 all-age observations and 6,105 age-specific observations.

---

## 3. Business / Analytical Questions

1. How did the country-average suicide rate change from 2000 to 2021?
2. Is the trend different by sex?
3. Which age groups have the highest observed rates?
4. Which countries have the highest and lowest all-age rates in the latest year?
5. Which countries experienced the largest absolute change between 2000 and 2021?
6. How large is the male–female rate gap?
7. Is GDP per capita associated with the observed suicide rate?
8. Where are data-quality limitations that could affect interpretation?

---

## 4. Key Findings

### 4.1 Long-term trend

The **country-average all-age rate** declined from approximately **10.40 per 100,000 in 2000** to **8.55 in 2021**, an approximate **17.8% decline** over the period.

A population-weighted calculation also declines over the period, from about **12.51 to 9.13 per 100,000**. The weighted and unweighted trends differ because countries have very different population sizes.

### 4.2 Sex disparity

Across the all-age observations, the mean rates are approximately:

- Male: **14.56 per 100,000**
- Female: **4.56 per 100,000**
- Both sexes: **9.53 per 100,000**

The male rate is therefore substantially higher than the female rate in this dataset. This is a key segmentation variable for any resource-allocation or prevention analysis.

### 4.3 Age pattern

In the latest year, the average rate increases markedly with age:

- 10–19: ~3.64
- 15–19: ~6.12
- 20–29: ~9.35
- 40–49: ~12.25
- 60–69: ~16.06
- 70+: ~24.29

The 70+ group has the highest average rate among the age brackets supplied.

### 4.4 Latest-year country variation

In 2021, the highest all-age country-level observations include:

- Lesotho — 28.66
- Korea, Republic of — 27.53
- Eswatini — 27.23
- Guyana — 24.78
- Uruguay — 24.75

The lowest observed values include:

- Saint Vincent and the Grenadines — 0.41
- Syrian Arab Republic — 0.59
- Jordan — 0.60
- Egypt — 0.63
- Palestine, State of — 0.65

These are descriptive dataset values, not judgments about countries or populations.

### 4.5 Country-level change

Largest decreases in the all-age rate between 2000 and 2021 include:

- Russian Federation: -31.69
- Lithuania: -28.28
- Sri Lanka: -24.16
- Belarus: -23.89
- Latvia: -19.61

Largest increases include:

- Lesotho: +15.98
- Eswatini: +14.70
- Korea, Republic of: +12.47
- South Africa: +9.17
- Uruguay: +8.40

The change analysis is more informative than a single-year ranking because it identifies countries with substantially different trajectories.

### 4.6 GDP relationship

The Pearson correlation between all-age suicide rate and GDP per capita is approximately **+0.15** across the available country-year observations; using log GDP per capita gives approximately **+0.20**.

This is a **weak positive association**, not evidence that GDP causes higher suicide rates. Other variables—age structure, sex composition, reporting practices, social conditions, access to services, inequality, substance use, conflict, and many other factors—can affect observed rates.

### 4.7 Data-quality considerations

There are **315 rows with missing GDP and GDP-per-capita values**, concentrated in five countries in the dataset:

- Cuba
- Eritrea
- Korea, Democratic People's Republic of
- South Sudan
- Yemen

The suicide-rate and population fields are complete in the supplied file.

---

## 5. Recommended Business / Policy Insights

### Insight 1 — Use trend monitoring rather than single-year rankings

A dashboard should track:
- current rate
- 5-year change
- 2000-to-latest change
- sex gap
- age profile

This reduces the risk of treating one year's value as the complete story.

### Insight 2 — Segment interventions by demographic group

The persistent male–female difference and higher rates among older age groups indicate that a single undifferentiated strategy would hide important population-level differences.

For analytics teams, the dashboard should therefore support filtering by:
- sex
- age bracket
- country
- year

### Insight 3 — Prioritize trajectory analysis

Countries with large increases deserve a different analytical workflow from countries with high but declining rates.

A useful KPI framework is:

**Current level + direction of change + demographic gap + data quality**

rather than current level alone.

### Insight 4 — Do not use GDP as a standalone explanatory variable

GDP per capita has only a weak correlation with the rate in this dataset. Economic size should therefore be treated as one contextual variable rather than a causal explanation.

### Insight 5 — Separate measurement issues from real-world changes

Before interpreting a large country-to-country difference, analysts should validate:
- data definitions
- estimation methodology
- reporting completeness
- population denominators
- changes in data collection
- age standardization

---

## 6. SQL Analysis

`analysis_queries.sql` contains PostgreSQL-compatible queries covering:

- dataset profiling
- missing-data checks
- annual trend
- population-weighted trend
- country rankings
- sex comparison
- male–female gap
- age analysis
- 2000 vs latest-year change
- GDP correlation
- missing-data country audit
- duplicate detection
- high-rate observations

---

## 7. Python Analysis

`global_suicide_rates_analysis.py` performs:

### EDA
- shape and data types
- missing values
- duplicates
- categorical distributions
- descriptive statistics
- negative/zero-value checks

### Analysis
- annual trend
- sex trend
- age profile
- latest-year country ranking
- GDP relationship
- country-level change
- male–female gap

### Visualizations

The script generates 8 PNG files:

1. `01_annual_trend.png`
2. `02_sex_trend.png`
3. `03_age_profile_latest_year.png`
4. `04_top15_latest_year.png`
5. `05_bottom10_latest_year.png`
6. `06_gdp_vs_rate.png`
7. `07_country_change_2000_2021.png`
8. `08_gender_gap_latest_year.png`

## 8. Suggested Portfolio Statement

> **Global Suicide Rates — SQL & Python Analytics:** Conducted an end-to-end analysis of 18K+ country-year demographic observations across 185 countries, identifying long-term trend changes, demographic disparities, country-level trajectories, and socioeconomic relationships. Built PostgreSQL-compatible analytical queries and Python EDA/visualizations, with explicit data-quality checks and non-causal interpretation of socioeconomic correlations.

---

## 9. Conclusion

This project demonstrates that a strong analytics solution should move beyond simply reporting the highest or lowest values.

The dataset shows a broad long-term decline in the country-average all-age suicide rate from 2000 to 2021, while substantial differences remain across sex, age groups, and countries. The male rate is considerably higher than the female rate, and the oldest age group has the highest average observed rate. Country-level trajectories also vary significantly, with some countries showing large declines and others substantial increases.

From a senior-analyst perspective, the most important takeaway is that **trend, segmentation, trajectory, and data quality should be evaluated together**. GDP per capita alone provides only a weak association and should not be interpreted as a causal driver.
