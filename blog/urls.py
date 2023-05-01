from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.postList, name='postList'),
    path('<int:id>/', views.postDetails, name='postDetails'),
]
