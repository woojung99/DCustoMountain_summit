from django.urls import path 
from cal import views 

app_name = "cal" 
urlpatterns = [
    path("", views.CalendarView.as_view(), name="calendar"), 
    path("calendar/<int:calendar_id>/", views.calendar_detail, name="calendar_detail"), 
    path("add_calendar/", views.add_calendar, name="add_calendar"), 
    path("edit_calendar/<int:calendar_id>/", views.edit_calendar, name="edit_calendar"), 
    path("delete_calendar/<int:calendar_id>/", views.delete_calendar, name="delete_calendar"), 
]