from django.urls import path 
from cal import views 

app_name = "cal" 
urlpatterns = [
    path("", views.CalendarView.as_view(), name="calendar"), 
    # path("detail/<int:id>/", views.CalendarDetailView.as_view(), name="calendar_detail"), 
]