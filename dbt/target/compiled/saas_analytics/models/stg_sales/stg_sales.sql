

WITH raw_data AS(
    SELECT *
    FROM `sam-dafs-16`.`aws_sales_saas`.`aws_sales`
),

-- Nettoyage et type cast
cleaned AS (
    SELECT
        DISTINCT  -- supprime exactement les doublons
        CAST(`Row ID` AS INT64) AS row_id,
        `Order ID` AS order_id,
        CAST(`Order Date` AS DATE) AS order_date,  -- conversion en date
        CAST(`Date Key` AS INT64) AS date_key,
        `Contact Name` AS contact_name,
        UPPER(`Country`) AS country,
        `City` AS city,
        `Region` AS region,
        `Subregion` AS subregion,
        `Customer` AS customer_name,
        CAST(`Customer ID` AS INT64) AS customer_id,
        `Industry` AS industry,
        `Segment` AS segment,
        `Product` AS product,
        `License` AS license,
        COALESCE(`Sales`, 0) AS sales,           -- gérer valeurs manquantes
        COALESCE(`Quantity`, 0) AS quantity,
        COALESCE(`Discount`, 0) AS discount,
        COALESCE(`Profit`, 0) AS profit
    FROM raw_data
),

-- Colonnes temporelles
with_date AS (
    SELECT
        *,
        EXTRACT(DAY FROM order_date) AS day,
        EXTRACT(MONTH FROM order_date) AS month,
        EXTRACT(YEAR FROM order_date) AS year,
        EXTRACT(DAYOFWEEK FROM order_date) AS weekday,   -- 1=Sunday, 7=Saturday
        FORMAT_DATE('%A', order_date) AS day_name,
        EXTRACT(QUARTER FROM order_date) AS quarter,
        FORMAT_DATE('%B', order_date) AS month_name,
        sales * (1 - discount) AS net_sales
    FROM cleaned
)

SELECT *
FROM with_date