

WITH 
stg_sales AS(
    SELECT * 
    FROM `sam-dafs-16`.`dbt_splassmann`.`stg_sales`
),

product_metrics AS(
    SELECT 
        product,
        SUM(net_sales) as product_sales,
        SUM(profit) as product_profit,
        SUM(quantity) as product_quantity
    FROM stg_sales
    GROUP BY product
)

SELECT *
FROM product_metrics