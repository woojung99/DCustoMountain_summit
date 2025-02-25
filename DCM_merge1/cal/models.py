from django.db import models
from users.models import User 
from mountains.models import Mountain 
from datetime import date 

# Create your models here.
class CalendarContents(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE) 
    hikedate = models.DateField("등산 날짜", default=date.today)
    distance = models.FloatField("등산한 거리", blank=True) 
    duration = models.DurationField("등산한 시간", blank=True) 
    memo = models.TextField("기타", blank=True) 

    def __str__(self): 
        return f"{self.mountain} ({self.hikedate})"
    