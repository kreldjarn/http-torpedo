from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField

class TestRun(models.Model):
    user = models.ForeignKey(User)
    json = JSONField()
