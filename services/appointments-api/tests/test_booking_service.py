from unittest.mock import MagicMock, patch

import pytest

from brightwell_appointments.services.booking_service import BookingService, PatientRestricted


def test_restricted_patient_cannot_book(patients):
    svc = BookingService(MagicMock())
    svc.patients = MagicMock()
    svc.patients.find_by_identity.return_value = MagicMock(id=7)
    req = MagicMock()
    req.patient.postcode = None
    req.patient.eircode = None
    with patch("brightwell_appointments.services.booking_service.NoShowPolicy") as nsp:
        nsp.return_value.is_restricted.return_value = True
        with pytest.raises(PatientRestricted):
            svc.book(req, MagicMock())
