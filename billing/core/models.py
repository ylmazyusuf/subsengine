from django.db import models
from django.db.models import fields, Q
from django.db.models.functions import Lower


class TimeStampModel(models.Model):
    created_at = fields.DateTimeField(auto_now_add=True)
    updated_at = fields.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LowerEmailQuerySet(models.QuerySet):
    def filter(self, *args, **kwargs):
        if 'email' in kwargs and isinstance(kwargs['email'], str):
            kwargs['email'] = kwargs['email'].lower()
        return super().filter(*args, **kwargs)


class Merchant(TimeStampModel):
    email = fields.EmailField(unique=True, )
    is_active = fields.BooleanField(default=False)
    objects = LowerEmailQuerySet.as_manager()

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
