from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# class Work(models.Model):
#     Meter_No = models.CharField(max_length=15)
#     feeder_name = models.CharField(max_length=15)
#     job_type = models.CharField(max_length=40)
#     job_description = models.TextField(max_length=1000)
#     CT_analysis = models.FileField(null=True,blank=True,upload_to='Analysis/')
#     VT_analysis = models.FileField(null=True,blank=True,upload_to='Analysis/')
#     Energy_Meter_Analysis = models.FileField(null=True,blank=True,upload_to='Analysis/')
#     field_report = models.FileField(null=True,blank=True,upload_to='Analysis/')
#
# class changePW(models.Model):
#     old_password = models.CharField(max_length=20)
#     new_password = models.CharField(max_length=20)
