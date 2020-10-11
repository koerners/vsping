from django.contrib import admin


# Register your models here.
from sitechecker.models import Job


class JobAdmin(admin.ModelAdmin):
    pass
admin.site.register(Job, JobAdmin)