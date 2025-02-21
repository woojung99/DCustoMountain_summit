from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
class User(AbstractUser): 
    profile_image = models.ImageField(upload_to="users/profile", blank=True)
    short_description = models.TextField(blank=True) 

    def __str__(self): 
        return self.username 
