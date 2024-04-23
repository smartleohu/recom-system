from django.contrib import admin

from recom_system.app import models

admin.site.register(models.UserProfile)
admin.site.register(models.Anomaly)
admin.site.register(models.PowerComponent)
