from datetime import datetime

from django.db import models


# Create your models here.
class Counters(models.Model):
    id = models.AutoField
    count = models.IntegerField(max_length=11, default=0)
    createdAt = models.DateTimeField(default=datetime.now(), )
    updatedAt = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Counters'

class User(models.Model):
    id = models.AutoField
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    user_type = models.IntegerField(max_length=11)

class Event(models.Model):
    id = models.AutoField
    content = models.TextField()
    comment = models.TextField()
    create_time = models.DateTimeField(max_length=128)

    status = models.IntegerField(max_length=11)