from django import views
from django.urls import path
from . views import *
from . import views
urlpatterns = [
    path("post/" , PostView.as_view() ),
    path("post_update/<int:pk>/" , PostView.as_view() ),
    path("friends/" , FriendsView.as_view() ),
    path("search/<str:key>/" , FriendsView.search ),
    path("friends_req_update/<int:pk>/" , FriendsView.as_view() ),
    path("like/" , LikeView.as_view() ),
    path("update_like/<int:pk>/" , LikeView.as_view() ),
    path("comment/" , CommentView.as_view() ),
    path("comment/<int:pk>/" , CommentView.as_view() ),


]