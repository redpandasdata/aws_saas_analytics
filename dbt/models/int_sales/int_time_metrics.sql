{{ config(materialized='view') }}

WITH 
stg_sales AS(
    SELECT * 
    FROM {{ref('stg_sales')}}
),


time_metrics AS (
    WITH monthly_sales AS (

        SELECT
            year,
            month,
            quarter,
            SUM(net_sales) AS month_sales
        FROM stg_sales
        GROUP BY year, month, quarter

    )

    SELECT
        *,
        SUM(month_sales) OVER(PARTITION BY year) AS year_sales
    FROM monthly_sales
)

SELECT *
FROM time_metrics
