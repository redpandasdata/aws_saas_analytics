WITH 
customer AS(
    SELECT *
    FROM `sam-dafs-16`.`dbt_splassmann`.`int_customer_metrics`
),

rfm AS(
    SELECT
    customer_name,
    DATE_DIFF(CURRENT_DATE(), customer.last_date_order, DAY) as recency,
    customer.order_count as frequency,
    customer.total_sales as monetary
    FROM customer
),

rfm_scores AS(
    SELECT
    customer_name,
    recency,
    frequency,
    monetary,
    NTILE(4) OVER (ORDER BY frequency DESC) as f_score,
    NTILE(4) OVER( ORDER BY recency ASC) as r_score,
    NTILE(4) OVER (ORDER BY monetary DESC) as m_score
    FROM rfm
),

rfm_segment AS(
    SELECT
        *,
        CASE
            WHEN r_score = 4 AND f_score = 4 AND m_score = 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
            WHEN r_score = 1 THEN 'At Risk'
            ELSE 'Potential'
        END AS rfm_segment
    FROM rfm_scores
)

SELECT 
    customer.customer_name,
    customer.industry,
    customer.segment,
    customer.country,
    customer.order_count,
    customer.total_sales,
    customer.total_profit,
    customer.first_date_order,
    customer.last_date_order,
    customer.diff_date,
    customer.total_sales / NULLIF(customer.diff_date,0) * 30 as ltv,
    customer.total_sales / customer.order_count as average_order_value,
    rfm.recency,
    rfm.frequency,
    rfm.monetary,
    rfm.r_score,
    rfm.f_score,
    rfm.m_score,
    rfm.rfm_segment
FROM customer
LEFT JOIN rfm_segment rfm ON customer.customer_name = rfm.customer_name