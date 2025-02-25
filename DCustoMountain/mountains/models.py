from django.db import models

# Create your models here.
class Mountain(models.Model):
    location = models.CharField(max_length=100) # 지역
    name = models.CharField(max_length=50) # 산이름
    height = models.FloatField() # 산높이
    mtn_difficulty = models.CharField(max_length=100) # 난이도
    leadtime = models.CharField(max_length=100) # 소요시간


    def __str__(self):
        return self.name 
    