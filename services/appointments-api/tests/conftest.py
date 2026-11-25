import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def patients():
    return json.loads((FIXTURES / "patients.json").read_text())


@pytest.fixture
def appointments():
    return json.loads((FIXTURES / "appointments.json").read_text())
