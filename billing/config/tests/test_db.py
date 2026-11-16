import pytest
from django.db import connection

@pytest.mark.django_db
def test_database_smoke():
    """[teknik] Sağlanan DATABASE_URL ile database bağlantısı kurulabilir"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        db_result, = cursor.fetchone()
    assert db_result == 1
