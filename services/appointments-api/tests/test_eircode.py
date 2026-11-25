import pytest

from brightwell_appointments.services.eircode import normalise_eircode


def test_adds_space():
    assert normalise_eircode("x00x001") == "X00 X001"


def test_rejects_short():
    with pytest.raises(ValueError):
        normalise_eircode("X00X00")
