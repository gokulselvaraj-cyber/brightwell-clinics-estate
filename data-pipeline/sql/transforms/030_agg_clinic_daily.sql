-- build_clinic_daily: per clinic per day counts and DNA (did-not-attend) rate
DELETE FROM rpt.agg_clinic_daily WHERE visit_date >= current_date - 3;

INSERT INTO rpt.agg_clinic_daily (clinic_code, visit_date, booked, attended, no_shows, late_cancels,
                                  dna_rate, revenue)
SELECT clinic_code,
       visit_date,
       count(*) FILTER (WHERE status IN ('BOOKED', 'ARRIVED', 'SEEN', 'NO_SHOW')),
       count(*) FILTER (WHERE status = 'SEEN'),
       count(*) FILTER (WHERE status = 'NO_SHOW'),
       count(*) FILTER (WHERE is_late_cancel),
       round(count(*) FILTER (WHERE status = 'NO_SHOW')::numeric
             / nullif(count(*) FILTER (WHERE status IN ('SEEN', 'NO_SHOW')), 0), 4),
       coalesce(sum(tariff_price), 0)
  FROM rpt.fact_visit
 WHERE visit_date >= current_date - 3
 GROUP BY clinic_code, visit_date;
