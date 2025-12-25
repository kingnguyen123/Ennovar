-- SQLite
        SELECT
            SUM(t.[Line Total]) AS total_sales
        FROM transactions t
        JOIN products p
            ON t.product_id = p.product_id
        WHERE p.category = 'Feminine'
          AND p.sub_category='Coats and Blazers'
          AND t.Date >= '2023-01-01'
          AND t.Date <  '2023-12-31';
    

