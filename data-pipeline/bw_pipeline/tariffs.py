"""Maps staged procedure codes to specialty, tariff band and price (journey hop map_procedure_codes).

Prices for Irish clinics (EUR) get the ROI uplift from the reference module.
"""
from decimal import Decimal

from airflow.providers.postgres.hooks.postgres import PostgresHook

from .reference.procedure_codes import BAND_PRICE_GBP, ROI_TARIFF_UPLIFT, lookup

IRISH_PREFIXES = ("BW-DUB", "BW-DLR", "BW-CRK", "BW-GWY", "BW-LIM", "BW-KKY")


def price_for(procedure_code: str, clinic_code: str, payer: str = "SELF") -> Decimal:
    proc = lookup(procedure_code, payer)
    price = BAND_PRICE_GBP[proc.band]
    if clinic_code.startswith(IRISH_PREFIXES):
        price = (price * ROI_TARIFF_UPLIFT).quantize(Decimal("0.01"))
    return price


def map_staged_procedures(conn_id: str, **_) -> int:
    hook = PostgresHook(postgres_conn_id=conn_id)
    rows = hook.get_records("select id, procedure_code, clinic_code from rpt.stg_appointment "
                            "where procedure_code is not null")
    updates = [(lookup(code).specialty, lookup(code).band, price_for(code, clinic), rid)
               for rid, code, clinic in rows]
    hook.run("create temp table if not exists tmp_tariff (specialty text, band text, price numeric, id bigint)")
    hook.insert_rows("tmp_tariff", updates)
    hook.run("""update rpt.stg_appointment s set tariff_specialty = t.specialty, tariff_band = t.band,
                tariff_price = t.price from tmp_tariff t where t.id = s.id""")
    return len(updates)
