from django.db import models
from django.db.models import fields, Q
from django.db.models.functions import Lower


class TimeStampModel(models.Model):
    created_at = fields.DateTimeField(auto_now_add=True)
    updated_at = fields.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LowerCaseEmailField(models.EmailField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value


class Merchant(TimeStampModel):
    email = LowerCaseEmailField(unique=True, )
    is_active = fields.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(email=''),
                name='merchant_email_empty_condition'
            ),
            models.UniqueConstraint(
                Lower('email'),
                name='merchant_email_lower_unique'
            )
        ]
