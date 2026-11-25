from datetime import datetime, timezone
from unittest.mock import MagicMock

from brightwell_appointments.services.check_in_service import FALLBACK_OPEN_MINUTES, CheckInService


def _svc(setting):
    svc = CheckInService(MagicMock())
    svc.settings = MagicMock()
    svc.settings.get_int.side_effect = lambda key, default: setting if setting is not None else default
    return svc


def test_window_uses_setting():
    start = datetime(2026, 5, 1, 10, 0, tzinfo=timezone.utc)
    opens, closes = _svc(45).window(start)
    assert opens.minute == 15 and closes.minute == 15


def test_fallback_when_setting_missing():
    start = datetime(2026, 5, 1, 10, 0, tzinfo=timezone.utc)
    opens, _ = _svc(None).window(start)
    assert (start - opens).seconds == FALLBACK_OPEN_MINUTES * 60
