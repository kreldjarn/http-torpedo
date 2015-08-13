from django.db import models

from jsonfield import JSONField

# Create your models here.
class TestRun(models.Model):
    json = JSONField()
