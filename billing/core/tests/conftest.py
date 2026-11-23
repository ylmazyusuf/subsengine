import pytest
from core.models import Merchant

@pytest.fixture
def merchant(db):
    merchant = Merchant(email='ali@x.com')
    merchant.save()
    yield merchant
    merchant.delete()
