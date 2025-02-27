from django.urls import path 
from cal import views 

app_name = "cal" 
urlpatterns = [
    path("", views.calendar_view, name="calendar"), 
    path("event/<int:event_id>/", views.event_detail, name="event_detail"), 
    path("back_calendar/<int:event_id>/", views.back_calendar, name="back_calendar"), 
    path("add_event/", views.add_event, name="add_event"), 
    path("edit_event/<int:event_id>/", views.edit_event, name="edit_event"), 
    path("delete_event/<int:event_id>/", views.delete_event, name="delete_event"), 
]