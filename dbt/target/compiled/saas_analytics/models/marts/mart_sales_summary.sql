


WITH sales AS (
    SELECT * 
    FROM `sam-dafs-16`.`dbt_splassmann`.`stg_sales`
),

monthly_sales AS (
    SELECT
        DATE(year, month, 1) as month_date,
        year,
        month,
        quarter,
        SUM(net_sales) as revenue_month,
        SUM(quantity) as total_quantity,
        COUNT(*) as total_orders,
        COUNT(DISTINCT customer_name) as active_customers
    FROM sales
    GROUP BY year, month, quarter
),

first_orders AS (
    SELECT
        customer_name,
        MIN(order_date) as first_order_date
    FROM sales
    GROUP BY customer_name
),

new_customers AS (
    SELECT
        EXTRACT(YEAR FROM f.first_order_date) as year,
        EXTRACT(MONTH FROM f.first_order_date) as month,
        COUNT(DISTINCT f.customer_name) as new_customers
    FROM first_orders f
    GROUP BY year, month
)

SELECT
    m.year,
    m.month,
    m.quarter,
    DATE(m.year, m.month, 1) as month_date,
    COALESCE(m.revenue_month,0) as revenue_month,
    SUM(m.revenue_month) OVER(PARTITION BY m.year) as revenue_year,
   (m.revenue_month - LAG(m.revenue_month) OVER(ORDER BY m.year, m.month)) / NULLIF(LAG(m.revenue_month) OVER(ORDER BY m.year, m.month),0) as growth_rate,
    m.total_quantity,
    m.total_orders,
    m.active_customers,
    COALESCE(n.new_customers,0) as new_customers,
    COALESCE(m.revenue_month,0) / NULLIF(m.total_orders,0) as avg_order_value
FROM monthly_sales m
LEFT JOIN new_customers n
ON m.year = n.year
AND m.month = n.month