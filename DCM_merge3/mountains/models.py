from django.db import models
import datetime

# Create your models here.
class Mountain(models.Model):
    name = models.CharField(max_length=50) 
    location = models.CharField(max_length=100) 
    height = models.FloatField() 
    leadtime = models.CharField(max_length=50, blank=True) 
    mtn_image = models.ImageField(upload_to="mountains/image/", blank=True)
    detail_info = models.TextField(blank=True) 

    def __str__(self):
        return self.name 
    