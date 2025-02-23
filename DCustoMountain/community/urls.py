from django.urls import path
from community import views

app_name = "community"
urlpatterns = [
    path("feeds/", views.feeds, name="feeds"),
    path("<int:post_id>", views.post_detail, name="post_detail"),
    path("add_post/", views.add_post, name="add_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),
    path("add_comment/", views.add_comment, name="add_comment"),
    path("edit_comment/<int:comment_id>/", views.edit_comment, name="edit_comment"),
    path("delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("tags/<str:tag_name>/", views.tags, name="tags"),

]
