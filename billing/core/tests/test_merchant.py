import pytest

from core.models import Merchant
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_merchant_is_passive_up_start(merchant):
    """
        `[MER-01]` Yeni merchant pasif olarak oluşuyor
    """
    assert merchant.is_active == False

@pytest.mark.django_db
def test_merchant_create_update_time(merchant):
    """
        `[GEN-04]` Oluşturma ve güncelleme zamanı doluyor, güncellemede `updated_at` değişiyor (Merchant güncellenebilen bir model)
    """
    assert merchant.created_at is not None
    assert merchant.updated_at is not None
    merchant.is_active = True
    merchant.save()
    assert merchant.created_at != merchant.updated_at

@pytest.mark.django_db
def test_merchant_email_required():
    """
        `[MER-03]` Email'siz merchant oluşmuyor
    """
    with pytest.raises(IntegrityError) as excinfo:
        merchant = Merchant()
        merchant.save()
    assert "violates check constraint" in str(excinfo.value)


@pytest.mark.django_db
def test_merchant_email_unique():
    """
        `[MER-03]` Aynı email ile ikinci bir merchant oluşmuyor
    """
    email = 'ali@x.com'
    with pytest.raises(IntegrityError) as excinfo:
        merchant_one = Merchant(email=email)
        merchant_one.save()

        merchant_two = Merchant(email=email)
        merchant_two.save()

    assert "violates unique" in str(excinfo.value)

@pytest.mark.django_db
def test_merchant_email_lower():
    """
        `[MER-05]` `Ali@x.com` ile kaydedilen email `ali@x.com` olarak saklanıyor
    """
    email = 'Ali@x.com'
    
    merchant = Merchant(email=email)
    merchant.save()

    merchant_qs = Merchant.objects.filter(email=email.lower())
    assert merchant_qs.count() == 1

@pytest.mark.django_db
def test_merchant_email_upper():
    """
        `[MER-05]` `ali@x.com` ile kaydedilen email `Ali@x.com` olarak filtrelenebiliyor.
    """
    email = 'Ali@x.com'
    
    merchant = Merchant(email=email.lower())
    merchant.save()

    merchant_qs = Merchant.objects.filter(email=email)
    assert merchant_qs.count() == 1

@pytest.mark.django_db
def test_merchant_email_lower_unique():
    """
        `[MER-05]` `Ali@x.com` kayıtlıyken `ali@x.com` ile ikinci merchant oluşmuyor
    """
    email_lower_x = 'Ali@x.com'
    email_upper_x = 'Ali@X.com'

    with pytest.raises(IntegrityError) as excinfo:
        merchant = Merchant(email=email_lower_x)
        merchant.save()

        merchant = Merchant(email=email_upper_x)
        merchant.save()

    assert "violates unique" in str(excinfo.value)
