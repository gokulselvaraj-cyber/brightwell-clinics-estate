"""Row-count and null checks run by the data-insight team after a load (manual, not in the DAG yet)."""
CHECKS = {
    "fact_visit_not_empty": "select count(*) > 0 from rpt.fact_visit where visit_date = current_date - 1",
    "no_orphan_attendees": """select count(*) = 0 from rpt.fact_visit f
                              left join rpt.dim_service_user u on u.service_user_key = f.attendee_id
                              where u.service_user_key is null""",
    "clinic_daily_has_all_clinics": "select count(distinct clinic_code) >= 30 from rpt.agg_clinic_daily",
}
