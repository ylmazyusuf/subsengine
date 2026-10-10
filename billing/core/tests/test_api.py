import pytest
from unittest.mock import patch
from django.db import OperationalError
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

def test_health_check_200():
    client = APIClient()
    response = client.get('/health/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {"status": "ok", "db": "ok"}

def test_health_check_503(caplog):
    with patch("core.views.connection.cursor", side_effect=OperationalError("Mock Error")):
        client = APIClient()
        response = client.get('/health/')
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert response.json() == {"status": "fail", "db": "fail"}
        core_views_records = [record for record in caplog.records if record.name == "core.views"]
        assert len(core_views_records) == 1
        assert core_views_records[0].levelname == "ERROR"
        assert core_views_records[0].exc_info[0] is OperationalError
