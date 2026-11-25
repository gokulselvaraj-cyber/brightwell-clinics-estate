from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from brightwell_appointments.services.cancellation_service import CancellationService


def _svc(hours):
    with patch("brightwell_appointments.services.cancellation_service.get_settings") as gs:
        gs.return_value.booking.late_cancel_hours = hours
        return CancellationService(MagicMock())


def test_late_inside_window():
    now = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)
    assert _svc(24).is_late(now + timedelta(hours=23), now)


def test_not_late_outside_window():
    now = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)
    assert not _svc(24).is_late(now + timedelta(hours=30), now)


def test_prod_window_48():
    now = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)
    assert _svc(48).is_late(now + timedelta(hours=30), now)
