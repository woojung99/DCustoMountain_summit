from django.db import models

# Create your models here.
class Mountain(models.Model):
    mountain = models.CharField(max_length=50) 
    location = models.CharField(max_length=100) 
    height = models.FloatField() 

    def __str__(self):
        return self.mountain 
    