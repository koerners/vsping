from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField()
    last_checked = models.DateField(null=True)
    last_change = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    url = models.URLField(max_length=100)
    name = models.CharField(max_length=100, null=True)
    check_every = models.CharField(max_length=100,
                                   choices=[('15', '15 Minutes'), ('30', '30 Minutes'), ('60', '1 Hours'),('180', '3 Hours'),('360', '6 Hours'),('720', '12 Hours')])
    check_until = models.DateField(null=True)
