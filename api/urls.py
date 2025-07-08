from django.urls import path
from . import views

urlpatterns = [
    path('tasks', views.task_list, name='task_list'),
    path('task/create', views.task_create, name='task_create'),
    path('task/toggle/<int:k>', views.task_toggle, name='task_toggle'),
    path('task/delete/<int:k>', views.task_delete, name='task_delete'),
    path('task/update/<int:k>', views.task_update, name='task_update'),
]