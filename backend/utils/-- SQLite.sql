-- SQLite
SELECT
            SUM(t.Quantity) AS "Current Inventory"
            FROM transactions t
            JOIN products p
                ON t.product_id = p.product_id
            WHERE p.category = 'Feminine'
            AND p.sub_category = 'Sportswear'
            AND t.Size = 'M';
        