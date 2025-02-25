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
    path("<int:user_id>/follow/", views.follow, name="follow"),
    path("<int:user_id>/report/", views.report_user, name="report_user"), 
]