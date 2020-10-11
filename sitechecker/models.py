from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Job(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField()
    last_checked = models.DateTimeField(null=True)
    last_change = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    url = models.URLField(max_length=100)
    name = models.CharField(max_length=100, null=True)
    check_every = models.CharField(max_length=100,
                                   choices=[('15', '15 Minutes'), ('30', '30 Minutes'), ('60', '1 Hours'),
                                            ('180', '3 Hours'), ('360', '6 Hours'), ('720', '12 Hours')])
    check_until = models.DateField(null=True)
    html_current = models.BinaryField(null=True)
    screenshot = models.BinaryField(null=True)
    similarity = models.DecimalField(null=True, default=1, decimal_places=2, max_digits=23)
    threshold = models.DecimalField(null=True, default=100, decimal_places=1, max_digits=23)
