from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.postList, name='postList'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.postDetails, name='postDetails'),
    path('<int:post_id>/share/', views.sharePost, name='sharePost'),
]
