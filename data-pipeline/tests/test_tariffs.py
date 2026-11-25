from decimal import Decimal

from bw_pipeline.reference.procedure_codes import BAND_PRICE_GBP, lookup


def test_lookup_known_code():
    pc = lookup("BWP-01000")
    assert pc.specialty == "DERM"


def test_legacy_code_remapped():
    assert lookup("OPD-DERM-01").code == "BWP-01000"


def test_bands_have_prices():
    assert all(isinstance(v, Decimal) for v in BAND_PRICE_GBP.values())
