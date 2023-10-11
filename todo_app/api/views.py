from todo_app.models import Todo
from todo_app.api.serializers import TodoSerializer
from rest_framework.views import APIView
from rest_framework import status
from todo_app.api.utilities import Sendresponse

# multiple classes
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
