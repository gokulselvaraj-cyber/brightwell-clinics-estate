from unittest.mock import MagicMock

from brightwell_appointments.services.noshow_policy import NO_SHOW_LIMIT, NoShowPolicy


def _policy(count):
    session = MagicMock()
    session.scalar.return_value = count
    return NoShowPolicy(session)


def test_limit_is_three():
    assert NO_SHOW_LIMIT == 3


def test_two_no_shows_can_book():
    assert not _policy(2).is_restricted(1)


def test_three_no_shows_restricted():
    assert _policy(3).is_restricted(1)
