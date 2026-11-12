import pytest
from django.db import connection

@pytest.mark.django_db
def test_database_smoke():
    db_result = 0
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_result, = cursor.fetchone()
    except:
        pass
    assert db_result == 1
