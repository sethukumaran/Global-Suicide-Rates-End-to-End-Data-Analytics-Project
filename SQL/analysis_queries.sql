-- Global Suicide Rates Analytics
-- Assumed table name: global_suicide_rates

-- 1. Basic profile
SELECT COUNT(*) AS rows,
       COUNT(DISTINCT country) AS countries,
       MIN(year) AS first_year,
       MAX(year) AS last_year
FROM global_suicide_rates;

-- 2. Missing-data audit
SELECT
    COUNT(*) FILTER (WHERE gdp_usd IS NULL) AS missing_gdp,
    COUNT(*) FILTER (WHERE gdp_per_capita_usd IS NULL) AS missing_gdp_per_capita,
    COUNT(*) FILTER (WHERE total_country_population IS NULL) AS missing_population
FROM global_suicide_rates;

-- 3. Annual country-average all-age rate
SELECT year,
       ROUND(AVG(suicide_rate_per_100k)::numeric, 2) AS avg_rate_per_100k
FROM global_suicide_rates
WHERE age_bracket = 'all_ages'
  AND sex = 'both'
GROUP BY year
ORDER BY year;

-- 4. Population-weighted annual rate
SELECT year,
       ROUND(
           SUM(suicide_rate_per_100k * total_country_population)
           / NULLIF(SUM(total_country_population), 0)
       , 2) AS population_weighted_rate
FROM global_suicide_rates
WHERE age_bracket = 'all_ages'
  AND sex = 'both'
GROUP BY year
ORDER BY year;

-- 5. Latest-year country ranking
WITH latest AS (
    SELECT MAX(year) AS latest_year
    FROM global_suicide_rates
)
SELECT country,
       country_code,
       suicide_rate_per_100k
FROM global_suicide_rates
WHERE year = (SELECT latest_year FROM latest)
  AND age_bracket = 'all_ages'
  AND sex = 'both'
ORDER BY suicide_rate_per_100k DESC;

-- 6. Top 15 countries in the latest year
WITH latest AS (
    SELECT MAX(year) AS latest_year FROM global_suicide_rates
)
SELECT country,
       ROUND(suicide_rate_per_100k::numeric, 2) AS rate_per_100k
FROM global_suicide_rates
WHERE year = (SELECT latest_year FROM latest)
  AND age_bracket = 'all_ages'
  AND sex = 'both'
ORDER BY suicide_rate_per_100k DESC
LIMIT 15;

-- 7. Male vs female trend
SELECT year,
       ROUND(AVG(suicide_rate_per_100k) FILTER (WHERE sex = 'male')::numeric, 2) AS male_rate,
       ROUND(AVG(suicide_rate_per_100k) FILTER (WHERE sex = 'female')::numeric, 2) AS female_rate
FROM global_suicide_rates
WHERE age_bracket = 'all_ages'
GROUP BY year
ORDER BY year;

-- 8. Latest-year male/female gap by country
WITH p AS (
    SELECT country,
           MAX(year) AS latest_year
    FROM global_suicide_rates
    GROUP BY country
),
s AS (
    SELECT country,
           sex,
           suicide_rate_per_100k
    FROM global_suicide_rates
    WHERE age_bracket = 'all_ages'
      AND year = (SELECT MAX(year) FROM global_suicide_rates)
      AND sex IN ('male', 'female')
)
SELECT country,
       MAX(suicide_rate_per_100k) FILTER (WHERE sex = 'male') AS male_rate,
       MAX(suicide_rate_per_100k) FILTER (WHERE sex = 'female') AS female_rate,
       MAX(suicide_rate_per_100k) FILTER (WHERE sex = 'male')
       - MAX(suicide_rate_per_100k) FILTER (WHERE sex = 'female') AS male_female_gap
FROM s
GROUP BY country
ORDER BY male_female_gap DESC;

-- 9. Latest-year age profile
SELECT age_bracket,
       ROUND(AVG(suicide_rate_per_100k)::numeric, 2) AS avg_rate
FROM global_suicide_rates
WHERE year = (SELECT MAX(year) FROM global_suicide_rates)
  AND sex = 'both'
GROUP BY age_bracket
ORDER BY avg_rate DESC;

-- 10. 2000 vs latest-year change by country
WITH country_year AS (
    SELECT country, year, suicide_rate_per_100k
    FROM global_suicide_rates
    WHERE age_bracket = 'all_ages'
      AND sex = 'both'
      AND year IN (2000, (SELECT MAX(year) FROM global_suicide_rates))
)
SELECT country,
       MAX(suicide_rate_per_100k) FILTER (WHERE year = 2000) AS rate_2000,
       MAX(suicide_rate_per_100k) FILTER (WHERE year = (SELECT MAX(year) FROM global_suicide_rates)) AS rate_latest,
       MAX(suicide_rate_per_100k) FILTER (WHERE year = (SELECT MAX(year) FROM global_suicide_rates))
       - MAX(suicide_rate_per_100k) FILTER (WHERE year = 2000) AS absolute_change
FROM country_year
GROUP BY country
ORDER BY absolute_change;

-- 11. GDP relationship
SELECT year,
       ROUND(CORR(suicide_rate_per_100k, gdp_per_capita_usd)::numeric, 3) AS corr_rate_gdppc
FROM global_suicide_rates
WHERE age_bracket = 'all_ages'
  AND sex = 'both'
  AND gdp_per_capita_usd IS NOT NULL
GROUP BY year
ORDER BY year;

-- 12. Countries with missing GDP data
SELECT DISTINCT country, country_code
FROM global_suicide_rates
WHERE gdp_usd IS NULL OR gdp_per_capita_usd IS NULL
ORDER BY country;

-- 13. Data-quality duplicate check
SELECT country, country_code, year, sex, age_bracket, COUNT(*) AS duplicate_count
FROM global_suicide_rates
GROUP BY country, country_code, year, sex, age_bracket
HAVING COUNT(*) > 1;

-- 14. High-rate observations for review
SELECT country, year, sex, age_bracket, suicide_rate_per_100k
FROM global_suicide_rates
WHERE suicide_rate_per_100k >= 50
ORDER BY suicide_rate_per_100k DESC;
