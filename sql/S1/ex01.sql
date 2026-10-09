-- 1. Payment vs customer average. For every payment, show the amount, 
-- the customer's average payment, and the difference between them.
SELECT 
       amount,
       avg(amount) OVER (PARTITION BY customer_id) AS avg_amount_per_customer,
       amount - avg(amount) OVER (PARTITION BY customer_id) AS diff_from_avg

FROM payment;

-- 2.. Customer share of store revenue. 
-- Show one row per customer with their total spend, their store's total revenue, 
-- and their percentage of that store's revenue.
--  Hint: GROUP BY first, then SUM(SUM(amount)) OVER (PARTITION BY store_id)
SELECT
       SUM(amount) AS total_spend,
       SUM(SUM(amount)) OVER (PARTITION BY store_id) AS store_revenue,
       SUM(amount) / SUM(SUM(amount)) OVER (PARTITION BY store_id) * 100 AS pct_of_store_revenue
FROM payment
JOIN customer USING (customer_id)
GROUP BY customer_id, store_id;    


-- Three ranks side by side. Rank all customers by total spend using ROW_NUMBER, RANK and DENSE_RANK. 
-- Find at least one place where the three give different results.
SELECT customer_id,
        SUM(amount) AS total_spend,
        ROW_NUMBER() OVER (ORDER BY SUM(amount) DESC) AS row_num,
        RANK() OVER (ORDER BY SUM(amount) DESC) AS rank_num,
        DENSE_RANK() OVER (ORDER BY SUM(amount) DESC) AS dense_rank_num
FROM payment
GROUP BY customer_id
ORDER BY total_spend DESC;

-- Top 3 longest films per category, including ties. 
-- Show the category name, title, length and rank.
with ranked_films AS (
    SELECT category.name AS category_name,
           film.title,
           film.length,
           RANK() OVER (PARTITION BY category.category_id ORDER BY film.length DESC) AS length_rank     
    FROM category
    JOIN film_category ON category.category_id = film_category.category_id
    JOIN film ON film_category.film_id = film.film_id
)
SELECT * from ranked_films
WHERE length_rank <= 3;

SELECT category.name AS category_name,
       film.title,
       film.length,
       RANK() OVER (PARTITION BY category.category_id ORDER BY film.length DESC) AS length_rank     
FROM category
JOIN film_category ON category.category_id = film_category.category_id
JOIN film ON film_category.film_id = film.film_id


