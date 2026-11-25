-- Clinic-days with a DNA rate above 20%
SELECT clinic_code, visit_date, dna_rate FROM rpt.agg_clinic_daily
 WHERE dna_rate > 0.20 AND visit_date >= current_date - 30 ORDER BY dna_rate DESC;
