from todo_app.models import Todo, User
from todo_app.api.serializers import TodoSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from todo_app.api.utilities import Sendresponse, generate_access_token
from django.contrib.auth.hashers import make_password, check_password

class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            if User.objects.filter(email=email).exists():
                status_code = status.HTTP_409_CONFLICT
                message = f"User with {email} already exists"
                response = Sendresponse(False, status_code, message, "")
                return (response)
            serializer.save(password=make_password(serializer.validated_data.get('password')))
            status_code = status.HTTP_201_CREATED
            message = "User created"
            response = Sendresponse(True, status_code, "The user has been successfully registered", "")
            return (response)
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal server error"
            response = Sendresponse(False, status_code, message, serializer.errors)
            return (response)

class Login(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        user_name = serializer.validated_data.get('username')
        pass_word = serializer.validated_data.get('password')
        # check if user exists in the database
        try:
            logged_user = User.objects.get(username=user_name)
        except Exception as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            message = "Login error"
            response = Sendresponse(False, status_code, message, str(e))
            return (response)
        password_check = check_password(pass_word, logged_user.password)
        if password_check:
            token = generate_access_token(logged_user)
            status_code = status.HTTP_200_OK
            message = "Login successful"
            response = Sendresponse(True, status_code, message, logged_user)
            response.set_cookie('access_token', value=token, httponly=True)
            return (response)
        else:
            status_code = status.HTTP_401_UNAUTHORIZED
            message = "Invalid credentials"
            response = Sendresponse(False, status_code, message, serializer.errors)
            return (response)

class Tasks(APIView):
    # get request
    def get(self, request):
        tasks = Todo.objects.all()
        serializer = TodoSerializer(tasks, many=True)
        message = "Successfully fetched all tasks"
        status_code = status.HTTP_200_OK
        response = Sendresponse(True, status_code, message, serializer.data)
        return (response)

    # post request
    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "Successfully created a new task"
            status_code = status.HTTP_201_CREATED
            response = Sendresponse(True, status_code, message, serializer.data)
            return (response)
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal server error"
            response = Sendresponse(False, status_code, message, serializer.errors)
            return (response)

# single class
class Task(APIView):
    def get(self, request, pk):
        try:
            task = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            message = f"Task with id {pk} not found"
            response = Sendresponse(False, status_code, message, "")
            return (response)
        serializer = TodoSerializer(task)
        status_code = status.HTTP_200_OK
        message = "Successfully fetched a task"
        response = Sendresponse(True, status_code, message, serializer.data)
        return (response)

    def put(self, request, pk):
        task = Todo.objects.get(pk=pk)
        serializer = TodoSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK
            message = f"Successfully updated task with an id of {pk}"
            response = Sendresponse(True, status_code, message, serializer.data)
            return (response)
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal server error"
            response = Sendresponse(False, status_code, message, serializer.errors)
            return (response)

    def delete(self, request, pk):
        task = Todo.objects.get(pk=pk)
        task.delete()
        status_code = status.HTTP_204_NO_CONTENT
        message = f"Successfully deleted task with an id of {pk}"
        response = Sendresponse(True, status_code, message, "")
        return (response)

    def patch(self, request, pk):
        task = Todo.objects.get(pk=pk)
        serializer = TodoSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK
            message = f"Successfully updated task with an id of {pk}"
            response = Sendresponse(True, status_code, message, serializer.data)
            return (response)
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal server error"
            response = Sendresponse(False, status_code, message, serializer.errors)
            return (response)
