"""
Global Suicide Rates — End-to-End Exploratory & Business/Policy Analytics
Dataset: global_suicide_rates_real_who_worldbank.csv



Outputs:
    visualizations/*.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "global_suicide_rates_real_who_worldbank.csv"
OUTPUT_DIR = "visualizations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_FILE)

# ---------- Basic EDA ----------
print("Shape:", df.shape)
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nCountries:", df["country"].nunique())
print("Years:", df["year"].min(), "to", df["year"].max())
print("Sex:", df["sex"].unique())
print("Age groups:", df["age_bracket"].unique())

print("\nNumeric summary:")
print(df.describe().T)

# Data quality checks
print("\nNegative rates:", (df["suicide_rate_per_100k"] < 0).sum())
print("Zero rates:", (df["suicide_rate_per_100k"] == 0).sum())

# ---------- Analysis base ----------
all_age = df[df["age_bracket"] == "all_ages"].copy()
both = all_age[all_age["sex"] == "both"].copy()

# ---------- 1. Annual trend ----------
annual = both.groupby("year", as_index=False)["suicide_rate_per_100k"].mean()

plt.figure(figsize=(10, 5))
plt.plot(annual["year"], annual["suicide_rate_per_100k"], marker="o")
plt.title("Country-Average All-Age Suicide Rate by Year")
plt.xlabel("Year")
plt.ylabel("Rate per 100,000")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_annual_trend.png", dpi=160)
plt.close()

# ---------- 2. Sex trend ----------
sex_trend = all_age.groupby(["year", "sex"], as_index=False)["suicide_rate_per_100k"].mean()
plt.figure(figsize=(10, 5))
for sex in ["both", "male", "female"]:
    x = sex_trend[sex_trend["sex"] == sex]
    plt.plot(x["year"], x["suicide_rate_per_100k"], marker="o", label=sex.title())
plt.title("Suicide Rate Trend by Sex — All Ages")
plt.xlabel("Year")
plt.ylabel("Rate per 100,000")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_sex_trend.png", dpi=160)
plt.close()

# ---------- 3. Age profile ----------
age_2021 = df[(df["year"] == df["year"].max()) & (df["sex"] == "both")]
age_2021 = age_2021.groupby("age_bracket", as_index=False)["suicide_rate_per_100k"].mean()
age_2021 = age_2021.sort_values("suicide_rate_per_100k")

plt.figure(figsize=(10, 6))
plt.barh(age_2021["age_bracket"], age_2021["suicide_rate_per_100k"])
plt.title("Average Suicide Rate by Age Group — Latest Year")
plt.xlabel("Rate per 100,000")
plt.ylabel("Age group")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_age_profile_latest_year.png", dpi=160)
plt.close()

# ---------- 4. Top countries ----------
latest_year = both["year"].max()
top = both[both["year"] == latest_year].nlargest(15, "suicide_rate_per_100k")

plt.figure(figsize=(10, 7))
plt.barh(top["country"][::-1], top["suicide_rate_per_100k"][::-1])
plt.title(f"Top 15 Countries by All-Age Suicide Rate — {latest_year}")
plt.xlabel("Rate per 100,000")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_top15_latest_year.png", dpi=160)
plt.close()

# ---------- 5. Bottom countries ----------
bottom = both[both["year"] == latest_year].nsmallest(10, "suicide_rate_per_100k")

plt.figure(figsize=(10, 6))
plt.barh(bottom["country"][::-1], bottom["suicide_rate_per_100k"][::-1])
plt.title(f"10 Lowest Countries by All-Age Suicide Rate — {latest_year}")
plt.xlabel("Rate per 100,000")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_bottom10_latest_year.png", dpi=160)
plt.close()

# ---------- 6. GDP per capita relationship ----------
gdp = both.dropna(subset=["gdp_per_capita_usd"]).copy()
gdp["log_gdp_per_capita"] = np.log1p(gdp["gdp_per_capita_usd"])

plt.figure(figsize=(9, 6))
plt.scatter(gdp["gdp_per_capita_usd"], gdp["suicide_rate_per_100k"], alpha=0.35)
plt.xscale("log")
plt.title(f"GDP per Capita vs All-Age Suicide Rate ({gdp['year'].min()}–{gdp['year'].max()})")
plt.xlabel("GDP per capita (USD, log scale)")
plt.ylabel("Rate per 100,000")
plt.grid(alpha=0.2)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_gdp_vs_rate.png", dpi=160)
plt.close()

# ---------- 7. Country change ----------
wide = both.pivot(index="country", columns="year", values="suicide_rate_per_100k")
wide["change_2000_2021"] = wide[2021] - wide[2000]
changes = wide["change_2000_2021"].dropna().sort_values()
selected = pd.concat([changes.head(10), changes.tail(10)])

plt.figure(figsize=(10, 8))
plt.barh(selected.index, selected.values)
plt.axvline(0, linewidth=1)
plt.title("Largest Country-Level Changes in All-Age Rate: 2000 vs 2021")
plt.xlabel("2021 rate minus 2000 rate")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/07_country_change_2000_2021.png", dpi=160)
plt.close()

# ---------- 8. Latest-year sex gap ----------
latest_sex = all_age[all_age["year"] == latest_year].pivot_table(
    index="country", columns="sex", values="suicide_rate_per_100k"
).dropna()
latest_sex["male_female_gap"] = latest_sex["male"] - latest_sex["female"]
gap = latest_sex["male_female_gap"].nlargest(15).sort_values()

plt.figure(figsize=(10, 7))
plt.barh(gap.index, gap.values)
plt.title(f"Largest Male–Female Rate Gaps — {latest_year}")
plt.xlabel("Male rate minus female rate, per 100,000")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/08_gender_gap_latest_year.png", dpi=160)
plt.close()

# ---------- Key metrics ----------
weighted_annual = both.groupby("year").apply(
    lambda x: np.average(x["suicide_rate_per_100k"], weights=x["total_country_population"])
)

print("\n--- Key findings ---")
print(f"Country-average rate: {annual.iloc[0]['suicide_rate_per_100k']:.2f} in {annual.iloc[0]['year']:.0f} "
      f"to {annual.iloc[-1]['suicide_rate_per_100k']:.2f} in {annual.iloc[-1]['year']:.0f}.")
print(f"Country-average percentage change: "
      f"{(annual.iloc[-1]['suicide_rate_per_100k'] / annual.iloc[0]['suicide_rate_per_100k'] - 1) * 100:.1f}%.")

sex_means = all_age.groupby("sex")["suicide_rate_per_100k"].mean()
print("Mean all-age rate by sex:")
print(sex_means)

age_latest_full = df[(df["year"] == latest_year) & (df["sex"] == "both")].groupby(
    "age_bracket"
)["suicide_rate_per_100k"].mean().sort_values(ascending=False)
print("\nLatest-year age profile:")
print(age_latest_full)

corr = gdp[["suicide_rate_per_100k", "gdp_per_capita_usd"]].corr().iloc[0, 1]
log_corr = gdp[["suicide_rate_per_100k", "log_gdp_per_capita"]].corr().iloc[0, 1]
print(f"\nPearson correlation with GDP per capita: {corr:.3f}")
print(f"Pearson correlation with log GDP per capita: {log_corr:.3f}")

print("\nPlots written to:", OUTPUT_DIR)
