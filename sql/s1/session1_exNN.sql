-- 1. Payment vs customer average. Show each payment's amount, 
-- the customer's average payment (AVG ... OVER) and the difference between the two.
SELECT customer_id, payment_id, amount, 
	ROUND(AVG(amount) OVER (PARTITION BY customer_id), 2) AS payment_customer_avg,
	amount - ROUND(AVG(amount) OVER (PARTITION BY customer_id), 2) AS diff_from_avg
FROM payment
WHERE customer_id = 1
ORDER BY customer_id, payment_id;

-- 2. Payment count beside each row. 
-- Show each payment with the number of payments that customer made in total (COUNT(*) OVER ...).

SELECT payment_id, amount, customer_id,
	COUNT(*) OVER(PARTITION BY customer_id) AS payment_count
FROM payment
ORDER BY customer_id, payment_id;

-- 3. Biggest payment per customer. Show each payment with the customer's largest payment beside it. 
-- Then use a CTE to keep only the rows where amount equals that maximum. 
-- Can a customer appear more than once? Why?

WITH max_payment_cte AS (
SELECT payment_id, customer_id, amount, 
	ROUND(MAX(amount) OVER(PARTITION BY customer_id), 2) AS max_payment
FROM payment
)
SELECT payment_id, customer_id, amount 
FROM max_payment_cte
WHERE amount = max_payment
ORDER BY customer_id, payment_id;

-- Verify exercise 1 with the join-to-subquery method, 
-- and confirm the numbers match for customer 1.
SELECT p.customer_id, p.payment_id, p.amount, av.customer_average, (p.amount - av.customer_average) as diff_from_avg
FROM payment p
JOIN 
(SELECT customer_id, AVG(amount) AS customer_average
FROM payment
GROUP BY customer_id) av
ON av.customer_id = p.customer_id
WHERE p.customer_id = 1;

-- Explain in your own words (2–3 sentences): what does PARTITION BY do that GROUP BY doesn't?
-- GROUP BY divide the results to be one row for each group, it changes the grain.
-- No other details could be added with GROUP BY.
-- Partition By keeps the original grain of the data, allows to aggregate over a group without losing the ability to add more details to the query