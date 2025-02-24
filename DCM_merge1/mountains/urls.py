from django.urls import path
from mountains import views

app_name = "mountains"
urlpatterns = [
    path("filter/", views.filter, name="filter"), 
    path("<int:mountain_id>/experienced/", views.experienced, name="experienced"), 
]