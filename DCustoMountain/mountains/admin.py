from django.contrib import admin
from mountains.models import Mountain 

# Register your models here.
@admin.register(Mountain) 
class MountainAdmin(admin.ModelAdmin): 
    pass 