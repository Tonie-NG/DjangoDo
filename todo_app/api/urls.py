from django.urls import path
from todo_app.api.views import Task, Tasks

urlpatterns = [
    path('', Tasks.as_view(), name='task_list'),
    path('<int:pk>', Task.as_view(), name='task')
]
