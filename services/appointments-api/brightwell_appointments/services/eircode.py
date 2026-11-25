"""Eircode handling for clinics in Ireland.

Láimhseáil Eircode: seacht gcarachtar, eochair ródúcháin (3) agus aitheantóir uathúil (4).
Ná stóráil an t-Eircode gan spás; taispeáin é le spás i gcónaí.
"""
import re

# Eochracha ródúcháin: litir + dhá dhigit, nó D6W (Baile Átha Cliath 6 Thiar)
_ROUTING = re.compile(r"^([AC-FHKNPRTV-Y][0-9]{2}|D6W)$")
_UNIQUE = re.compile(r"^[0-9AC-FHKNPRTV-Y]{4}$")


def normalise_eircode(value: str) -> str:
    v = value.replace(" ", "").upper()
    if len(v) != 7:
        raise ValueError("Eircode must have 7 characters")
    routing, unique = v[:3], v[3:]
    # Má theipeann ar an seiceáil, diúltaigh don áirithint; ná buail tuairim
    if not _ROUTING.match(routing) or not _UNIQUE.match(unique):
        raise ValueError("not a valid Eircode")
    return f"{routing} {unique}"
