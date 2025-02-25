from django.db import models

# Create your models here.
class Mountain(models.Model):
    location = models.CharField(max_length=100, null=True) # 지역
    name = models.CharField(max_length=50) # 산이름
    height = models.FloatField(null=True) # 산높이
    mtn_difficulty = models.CharField(max_length=100, null=True) # 난이도
    leadtime = models.CharField(max_length=100, null=True) # 소요시간


    def __str__(self):
        return self.name 
    