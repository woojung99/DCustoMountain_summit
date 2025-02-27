from django.urls import path
from mountains import views

app_name = "mountains"
urlpatterns = [
    path("infopage/", views.infopage, name="infopage"), 
    path("<int:mountain_id>/", views.mountain_detail, name="mountain_detail"), 
]