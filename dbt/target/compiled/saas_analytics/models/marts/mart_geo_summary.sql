

SELECT 
    country,
    region,
    subregion,
    city,
    SUM(net_sales) as revenue,
    SUM(profit) as profit,
    COUNT(*) as orders,
    COUNT(DISTINCT customer_name) as customers,
    SUM(net_sales)/COUNT(*) as avg_order_value,
    SUM(profit)/SUM(net_sales) as profit_margin
FROM `sam-dafs-16`.`dbt_splassmann`.`stg_sales`
GROUP BY 
    country,
    region,
    subregion,
    city