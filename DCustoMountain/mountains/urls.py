from django.urls import path
from mountains import views

urlpatterns = [
    path("filter/", views.filter, name="filter"), 
]