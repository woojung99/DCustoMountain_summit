from django.db import models
from users.models import User 
from mountains.models import Mountain 
from datetime import date 

# Create your models here.
class CalendarContents(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE) 
    hikedate = models.DateField("등산 날짜", default=date.today)
    distance = models.PositiveIntegerField("등산한 거리") 
    duration = models.DurationField("등산한 시간") 
    memo = models.TextField() 
    # experienced = models.BooleanField("가본 산", default=False)
    # wish = models.BooleanField("가보고 싶은 산", default=False)

    def __str__(self): 
        return f"{self.mountain} ({self.hikedate})"
    