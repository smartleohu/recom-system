from django.db import models


class UserProfile(models.Model):
    user_name = models.CharField(primary_key=True, max_length=100,
                                 default='DefaultUser')
    role = models.CharField(max_length=50, default='User')
    email = models.EmailField(default='defaultuser@example.com')

    objects = models.Manager()


class Anomaly(models.Model):
    anomaly_id = models.CharField(primary_key=True, max_length=50,
                                  default='00')
    description = models.TextField(default='DefaultDescription')
    severity = models.CharField(max_length=50, default='Low')
    timestamp = models.DateTimeField(null=True)
    user_names = models.ManyToManyField(UserProfile, related_name='anomalies')
    recommended_product = models.CharField(max_length=100, default='')

    objects = models.Manager()


class PowerComponent(models.Model):
    component_id = models.CharField(primary_key=True, max_length=50,
                                    default='00')
    name = models.CharField(max_length=100, default='DefaultName')
    location = models.CharField(max_length=100, default='DefaultLocation')
    status = models.CharField(max_length=50, default='DefaultStatus')
    component_type = models.CharField(max_length=50, default='DefaultType')
    anomalies = models.ManyToManyField(Anomaly, related_name='components')

    objects = models.Manager()
