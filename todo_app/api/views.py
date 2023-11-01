from todo_app.models import Todo
from todo_auth.models import User
from todo_app.api.serializers import TodoSerializer
from utilities.response import Sendresponse
from utilities.sendemail import send_email
from rest_framework.views import APIView
from rest_framework import status
import jwt
from datetime import datetime
# from celery.schedules import schedule


class Tasks(APIView):
    # get request
    def get(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "You're not Logged in", "")
            return response
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "Invalid credentials", str(e))
            return (response)
        serializer = TodoSerializer(data=request.data)
        try:
            logged_user = User.objects.get(id=payload['user_id'])
        except Exception as e:
            response = Sendresponse(False, status.HTTP_404_NOT_FOUND, "NOt found", str(e))
            return response

        tasks = Todo.objects.filter(user=logged_user)
        if not tasks:
            message = "User has no tasks"
            status_code = status.HTTP_204_NO_CONTENT
            response = Sendresponse(True, status_code, message, [])
            return (response)
        serializer = TodoSerializer(tasks, many=True)
        message = "Successfully fetched all tasks"
        status_code = status.HTTP_200_OK
        response = Sendresponse(True, status_code, message, serializer.data)
        return (response)

    # post request
    def post(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "You're not Logged in", "")
            return response
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "Invalid credentials", str(e))
            return (response)
        serializer = TodoSerializer(data=request.data)
        try:
            logged_user = User.objects.get(id=payload['user_id'])
        except Exception as e:
            response = Sendresponse(False, status.HTTP_404_NOT_FOUND, "Not found", str(e))
            return response
        if serializer.is_valid():
            serializer.save(user=logged_user)
            message = "Successfully created a new task"
            response_data = serializer.data
            status_code = status.HTTP_201_CREATED
            response = Sendresponse(True, status_code, message, response_data)
            emessage = "Your task has been created"
            esubject = "Task created"
            ereceiver = [logged_user.email]
            desired_datetime_str = response_data['to_be_completed']
            desired_datetime = datetime.strptime(desired_datetime_str, '%Y-%m-%d')
            desired_datetime = datetime.now()
            send_email.apply_async((emessage, esubject, ereceiver), eta=desired_datetime)
            print(response_data)
            return (response)
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal server error"
            response = Sendresponse(False, status_code, message, serializer.errors)
            return (response)

# single class
class Task(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('access_token')
        if not token:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "You're not Logged in", "")
            return response
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "Invalid credentials", str(e))
            return (response)
        serializer = TodoSerializer(data=request.data)
        try:
            logged_user = User.objects.get(id=payload['user_id'])
        except Exception as e:
            response = Sendresponse(False, status.HTTP_404_NOT_FOUND, "Not found", str(e))
            return response
        try:
            task = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            message = f"Task with id {pk} not found"
            response = Sendresponse(False, status_code, message, "")
            return (response)
        if task.user != logged_user:
            message = "You're not the owner of this task"
            status_code = status.HTTP_204_NO_CONTENT
            response = Sendresponse(True, status_code, message, [])
            return response

        serializer = TodoSerializer(task)
        status_code = status.HTTP_200_OK
        message = "Successfully fetched a task"
        response = Sendresponse(True, status_code, message, serializer.data)
        return (response)

    def put(self, request, pk):
        token = request.COOKIES.get('access_token')
        if not token:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "You're not Logged in", "")
            return response
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "Invalid credentials", str(e))
            return (response)
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                logged_user = User.objects.get(id=payload['user_id'])
            except Exception as e:
                response = Sendresponse(False, status.HTTP_404_NOT_FOUND, "NOt found", str(e))
                return response
            try:
                task = Todo.objects.get(pk=pk)
            except Todo.DoesNotExist:
                status_code = status.HTTP_404_NOT_FOUND
                message = f"Task with id {pk} not found"
                response = Sendresponse(False, status_code, message, "")
                return (response)
            if task.user != logged_user:
                message = "You're not the owner of this task"
                status_code = status.HTTP_204_NO_CONTENT
                response = Sendresponse(True, status_code, message, [])
                return response

            # serializer = TodoSerializer(task)
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
        token = request.COOKIES.get('access_token')
        if not token:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "You're not Logged in", "")
            return response
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "Invalid credentials", str(e))
            return (response)

        try:
            logged_user = User.objects.get(id=payload['user_id'])
        except Exception as e:
            response = Sendresponse(False, status.HTTP_404_NOT_FOUND, "NOt found", str(e))
            return response
        try:
            task = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            message = f"Task with id {pk} not found"
            response = Sendresponse(False, status_code, message, "")
            return (response)
        if task.user != logged_user:
            message = "You're not the owner of this task"
            status_code = status.HTTP_204_NO_CONTENT
            response = Sendresponse(True, status_code, message, [])
            return response
        task.delete()
        status_code = status.HTTP_204_NO_CONTENT
        message = f"Successfully deleted task with an id of {pk}"
        response = Sendresponse(True, status_code, message, "")
        return (response)

    def patch(self, request, pk):
        token = request.COOKIES.get('access_token')
        if not token:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "You're not Logged in", "")
            return response
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            response = Sendresponse(False, status.HTTP_401_UNAUTHORIZED, "Invalid credentials", str(e))
            return (response)
        serializer = TodoSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                logged_user = User.objects.get(id=payload['user_id'])
            except Exception as e:
                response = Sendresponse(False, status.HTTP_404_NOT_FOUND, "NOt found", str(e))
                return response
            try:
                task = Todo.objects.get(pk=pk)
            except Todo.DoesNotExist:
                status_code = status.HTTP_404_NOT_FOUND
                message = f"Task with id {pk} not found"
                response = Sendresponse(False, status_code, message, "")
                return (response)
            if task.user != logged_user:
                message = "You're not the owner of this task"
                status_code = status.HTTP_204_NO_CONTENT
                response = Sendresponse(True, status_code, message, [])
                return response

            # serializer = TodoSerializer(task)
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
