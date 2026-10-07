-- Part 1 · Warm-ups
-- 1. (Session 1) For each film, show title, rating, length 
-- and the average length of films with the same rating, rounded to 1 decimal.

SELECT title, rating, length,
	   ROUND(AVG(length) OVER (PARTITION BY rating), 1) AS avg_length
FROM film
ORDER By avg_length DESC, title;

-- 2. GROUP BY) Count films per rating, most films first.
SELECT rating,
		COUNT(*) AS film_count
FROM film
GROUP BY rating
ORDER BY film_count DESC;


-- 3. (Debugging) This query fails. Explain why in one sentence, then fix it two ways: once with GROUP BY and once with a window.

   SELECT customer_id, SUM(amount)
   FROM payment
   GROUP BY customer_id;

-- The query fails because payment_id is not included in the GROUP BY clause, 
-- and it is not an aggregate function.

-- fix1 with GROUP BY
SELECT customer_id, SUM(amount) AS total_amount
FROM payment
GROUP BY customer_id
ORDER BY customer_id;

-- fix 2 with window function
SELECT customer_id, payment_id, 
    SUM(amount) OVER (PARTITION BY customer_id) AS total_amount
FROM payment
ORDER BY customer_id,  payment_id;

-- Part 5 · Practice exercises
-- 1. Three ranks on price. 
-- ank all films by rental_rate (highest first) with all three functions. Describe in one sentence what you see. 
-- Hint: count how many different rental rates exist.
SELECT film_id,title, rental_rate,
-- IMPORTANT: When you use RANK or DENSE_RANK, you must include a second column in the ORDER BY clause to make the results deterministic. 
-- Otherwise, the database can return different results each time you run the query.
-- There are only 3 rental rates, so DENSE_RANK gives 1–3, 
-- RANK jumps after each block of ties, and ROW_NUMBER counts 1–1000.

       ROW_NUMBER() OVER (ORDER BY rental_rate DESC, film_id) AS row_num,
       RANK() OVER (ORDER BY rental_rate DESC) AS rank_num,
       DENSE_RANK() OVER (ORDER BY rental_rate DESC) AS dense_rank_num
FROM film
ORDER BY rental_rate DESC, film_id;

-- 2.Latest payment per customer. 
-- Return exactly one row per customer: customer_id, payment_id, payment_date, amount. 
-- Make it deterministic. This is the dbt deduplication pattern you'll write constantly.
WITH ranked_payments AS (
    SELECT customer_id, payment_id, payment_date, amount,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY payment_date DESC, payment_id DESC) AS row_num
    FROM payment
)
SELECT customer_id, payment_id, payment_date, amount
FROM ranked_payments
WHERE row_num = 1
ORDER BY customer_id;