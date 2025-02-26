from django.urls import path
from mountains import views

app_name = "mountains"
urlpatterns = [
    path("filter/", views.filter, name="filter"), 
    path("<int:mountain_id>/experienced/", views.experienced, name="experienced"), 
    path("search/", views.search_mtn_info, name="search_mtn_info"),
    path("search/details/<int:pk>/", views.search_mtn_details, name="search_mtn_details")
    

]