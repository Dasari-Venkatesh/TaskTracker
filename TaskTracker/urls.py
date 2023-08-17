from django.urls import path
from . import views
urlpatterns =[
    path('users/', views.user_list.as_view()),
    path('users/<int:pk>/', views.user_view.as_view()),
]

