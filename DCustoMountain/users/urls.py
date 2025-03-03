from django.urls import path
from users import views

app_name = "users"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("<int:user_id>/mypage/", views.mypage, name="mypage"), 
    path("<int:user_id>/profile/", views.profile, name="profile"),
    path("<int:user_id>/edit_profile/", views.edit_profile, name="edit_profile"), 
    path("like_list/", views.like_list, name="like_list"),
    path("comment_list/", views.comment_list, name="comment_list"), 
    path("save_list/", views.save_list, name="save_list"), 
    path("<int:user_id>/followers/", views.followers, name="followers"),
    path("<int:user_id>/following/", views.following, name="following"),
    path("<int:user_id>/short_description/", views.short_description, name="short_description"), 
    path("<int:user_id>/follow/", views.follow, name="follow"),
    # path("<int:target_user_id>/follow_me/", views.follow_me, name="follow_me"), 
    path("<int:user_id>/report/", views.report_user, name="report_user"), 
    path("<int:mountain_id>/experienced/", views.experienced, name="experienced"), 
    path("<int:mountain_id>/wish/", views.wish, name="wish"), 
    path("experienced_list/", views.experienced_list, name="experienced_list"), 
    path("wish_list/", views.wish_list, name="wish_list"), 
    path("add_experienced/", views.add_experienced, name="add_experienced"), 
    path("add_wish/", views.add_wish, name="add_wish"), 
    path("distance_list/", views.distance_list, name="distance_list"), 
    path("duration_list/", views.duration_list, name="duration_list"), 
]