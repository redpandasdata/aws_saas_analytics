

WITH sales AS (
    SELECT *
    FROM `sam-dafs-16`.`dbt_splassmann`.`stg_sales`
)

SELECT
    product,
    SUM(net_sales) AS product_sales,
    SUM(profit) AS product_profit,
    SUM(quantity) AS product_quantity,
    AVG(discount) AS avg_discount,
    AVG(net_sales) AS avg_order_value
FROM sales
GROUP BY product