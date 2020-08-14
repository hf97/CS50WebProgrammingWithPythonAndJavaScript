
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addpost", views.addPost, name="addPost"),
    path("editpost", views.editPost, name="editPost"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("u/<str:username>", views.profile, name="profile")
]
