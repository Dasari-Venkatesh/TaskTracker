from django.urls import path
from . import views
urlpatterns =[
    path('users/', views.user_list.as_view()),
    path('users/<int:pk>/', views.user_view.as_view()),
    path('tasks/', views.task_list.as_view()),
    path('tasks/<int:pk>/', views.task_view.as_view()),
    path('teams/', views.team_list.as_view()),
    path('teams/<int:pk>/', views.team_view.as_view()),

]

