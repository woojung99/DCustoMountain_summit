from django.contrib import admin
from cal.models import CalendarContents

# Register your models here.
@admin.register(CalendarContents) 
class CalendarContentsAdmin(admin.ModelAdmin): 
    pass 