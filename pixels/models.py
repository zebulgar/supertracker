from django.db import models

# Create your models here.

class Requests(models.Model):
	username = models.CharField(max_length=200)
	time_opened = models.DateTimeField('time opened')
	isp = models.CharField(max_length=200)
	client = models.CharField(max_length=200)
	os = models.CharField(max_length=200)
	device = models.CharField(max_length=200)
	region = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	country_name = models.CharField(max_length=200)
	latitude = models.CharField(max_length=200)
	longitude = models.CharField(max_length=200)