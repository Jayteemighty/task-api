from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
]