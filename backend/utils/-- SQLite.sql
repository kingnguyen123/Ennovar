-- SQLite
SELECT 
            CAST(strftime('%Y', MIN(t.transaction_date)) AS INTEGER) AS min_year,
            CAST(strftime('%Y', MAX(t.transaction_date)) AS INTEGER) AS max_year
        FROM transactions t

        