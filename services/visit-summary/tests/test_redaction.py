from brightwell_visit_summary.redaction import strip_identifiers


def test_nhs_number_removed():
    assert "[NHS-NUMBER]" in strip_identifiers("NHS 999 000 0001 seen today")


def test_ppsn_removed():
    assert "[PPSN]" in strip_identifiers("PPSN 0000001TA")


def test_name_is_not_removed():
    # documented gap DP-7: names pass through
    assert "Test01" in strip_identifiers("Test01 Patient attended")
