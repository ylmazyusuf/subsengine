from django.db import models
from django.db.models import fields, Q

class TimeStampModel(models.Model):
    created_at = fields.DateTimeField(auto_now_add=True)
    updated_at = fields.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Merchant(TimeStampModel):
    email = fields.EmailField()
    is_active = fields.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(email=''),
                name='merchant_email_empty_condition'
            )
        ]
