-- transform_noshow_flags: flag service users with repeated no-shows (attendance policy AP-3)
-- Uwaga: liczymy tylko NO_SHOW z ostatnich 12 miesięcy; LATE_CANCELLED się nie liczy.
-- (Polish note from the original author: only NO_SHOW in the last 12 months counts; late cancels do not.)
UPDATE rpt.dim_service_user u
   SET noshow_flag = (s.no_shows > 3)
  FROM (
        SELECT attendee_id, count(*) AS no_shows
          FROM rpt.fact_visit
         WHERE status = 'NO_SHOW'
           AND visit_date >= current_date - interval '12 months'
         GROUP BY attendee_id
       ) s
 WHERE s.attendee_id = u.service_user_key;
