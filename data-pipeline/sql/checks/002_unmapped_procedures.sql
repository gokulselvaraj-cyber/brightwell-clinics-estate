-- Staged procedure codes the reference module did not map
SELECT procedure_code, count(*) FROM rpt.stg_appointment
 WHERE procedure_code IS NOT NULL AND tariff_band IS NULL
 GROUP BY procedure_code ORDER BY 2 DESC;
