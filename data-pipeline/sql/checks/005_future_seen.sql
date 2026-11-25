-- SEEN appointments dated in the future (clock or status bug)
SELECT visit_key, visit_date FROM rpt.fact_visit WHERE status = 'SEEN' AND visit_date > current_date;
