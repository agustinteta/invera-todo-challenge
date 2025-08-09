from django.urls import path
from .views import task_list, task_create, task_toggle_complete, task_delete

urlpatterns = [
    path('list/', task_list, name='task-list'),
    path('create/', task_create, name='task-create'),
    path('<int:pk>/toggle_complete/', task_toggle_complete, name='task-toggle-complete'),
    path('<int:pk>/delete/', task_delete, name='task-delete'),
]