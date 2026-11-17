from django.db import models
from django.db.models import fields

# Create your models here.
class Merchant(models.Model):
    email = fields.EmailField()
