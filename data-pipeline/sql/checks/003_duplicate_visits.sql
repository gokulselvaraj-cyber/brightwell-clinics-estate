-- More than one fact row per appointment
SELECT visit_key, count(*) FROM rpt.fact_visit GROUP BY visit_key HAVING count(*) > 1;
