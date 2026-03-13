

WITH 
stg_sales AS(
    SELECT * 
    FROM `sam-dafs-16`.`dbt_splassmann`.`stg_sales`
),

customer_metrics AS(
    SELECT 
        customer_name as customer_name,
        ANY_VALUE(industry) as industry,
        ANY_VALUE(segment) as segment,
        ANY_VALUE(country) as country,
        COUNT(*) as order_count,
        SUM(net_sales) as total_sales,
        SUM(profit) as total_profit,
        SUM(quantity) as quantity_total_ordered,
        MIN(order_date) as first_date_order,
        MAX(order_date) as last_date_order,
        DATE_DIFF(MAX(order_date), MIN(order_date), DAY) as diff_date
    FROM stg_sales
    GROUP BY customer_name
 )

SELECT *
FROM customer_metrics