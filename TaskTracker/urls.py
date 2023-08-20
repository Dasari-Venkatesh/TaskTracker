from django.urls import path
from .views import (CustomUserListCreateView,
                    CustomUserRetrieveUpdateDestroyView,
                    task_list,
                    task_view,
                    team_list,
                    team_view
                )
urlpatterns =[
    path('users/', CustomUserListCreateView.as_view()),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view()),
    path('tasks/', task_list.as_view()),
    path('tasks/<int:pk>/', task_view.as_view()),
    path('teams/', team_list.as_view()),
    path('teams/<int:pk>/', team_view.as_view()),

]

