from django.urls import path
from todo_app.api.authview import Signup, Login
from todo_app.api.views import Task, Tasks

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path("login/", Login.as_view(), name='login'),
    path('', Tasks.as_view(), name='task_list'),
    path('<int:pk>', Task.as_view(), name='task')
]
