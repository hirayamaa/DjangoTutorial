from django.urls import path
from . import views

app_name = 'photo'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:pk>/', views.users_detail, name='users_detail'),
]
