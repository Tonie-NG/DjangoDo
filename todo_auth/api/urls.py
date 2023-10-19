
from django.urls import path
from todo_auth.api.views import Signup, Login

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path("login/", Login.as_view(), name='login'),
]
