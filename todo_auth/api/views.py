from todo_auth.models import User
from todo_auth.api.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from utilities.response import Sendresponse, generate_access_token
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError

class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
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
        except IntegrityError:
            status_code = status.HTTP_409_CONFLICT
            message = "User with this email or username already exists."
            response = Sendresponse(False, status_code, message, "")
            return response

class Login(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get('username')
            pass_word = serializer.validated_data.get('password')
            # check if user exists in the databasetry
            try:
                logged_user = User.objects.get(username=user_name)
            except Exception as e:
                status_code = status.HTTP_401_UNAUTHORIZED
                message = "Login error"
                response = Sendresponse(False, status_code, message, str(e))
                return (response)
            password_check = check_password(pass_word, logged_user.password)
            if password_check:
                access_token = generate_access_token(logged_user)
                user_data = UserSerializer(logged_user).data
                user_data['access_token'] = access_token
                status_code = status.HTTP_200_OK
                message = "Login successful"
                response = Sendresponse(True, status_code, message, user_data)
                response.set_cookie('access_token', value=access_token, httponly=True)
                return (response)
            else:
                status_code = status.HTTP_401_UNAUTHORIZED
                message = "Invalid credentials"
                response = Sendresponse(False, status_code, message, serializer.errors)
                return (response)
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal server error"
            response = Sendresponse(False, status_code, message, serializer.errors)
            return (response)
