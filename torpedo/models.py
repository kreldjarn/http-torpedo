from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField

class TestRun(models.Model):
    
    json = JSONField()
