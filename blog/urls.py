from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.postList, name='postList'),
    path('tag/<slug:tag_slug>/', views.postList, name='postList_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.postDetails, name='postDetails'),
    path('<int:post_id>/share/', views.sharePost, name='sharePost'),
    path('<int:post_id>/comment/', views.postComment, name='postComment'),
    path('feed/', LatestPostsFeed(), name='postFeed')
]


