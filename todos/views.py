from rest_framework.views import APIView  # Importing APIView for creating class-based views
from rest_framework.permissions import IsAuthenticated  # Importing permission to enforce authentication
from rest_framework.response import Response  # Importing Response to send API responses
from rest_framework import status  # Importing status codes for API responses
from .models import Todo  # Importing the Todo model
from .serializers import TodoSerializer  # Importing the Todo serializer
from rest_framework import viewsets


# Class-based view for managing todos
class TodoListView(APIView):  
    """
    Handles listing and creating todos for the authenticated user.
    """
    permission_classes = [IsAuthenticated]  # Enforce authentication for this view

    def get(self, request):
        """
        Fetches all todos for the authenticated user.
        """
        todos = Todo.objects.filter(user=request.user)  # Get todos owned by the current user
        serializer = TodoSerializer(todos, many=True)  # Serialize the todos
        return Response(serializer.data)  # Respond with the serialized data

    def post(self, request):
        """
        Creates a new todo for the authenticated user.
        """
        data = request.data  # Extract the input data from the request
        data['user'] = request.user.id  # Set the user field to the current user's ID
        serializer = TodoSerializer(data=data)  # Deserialize the input data
        if serializer.is_valid():  # Check if the input data is valid
            serializer.save()  # Save the todo to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Respond with the created todo data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Respond with validation errors

    def delete(self, request, todo_id):
        """
        Deletes a specific todo item for the authenticated user.
        """
        try:
            todo = Todo.objects.get(id=todo_id, user=request.user)  # Find the Todo by ID and ensure it belongs to the authenticated user
            todo.delete()  # Delete the todo
            return Response({"message": "Todo successfully deleted."}, status=status.HTTP_204_NO_CONTENT)  # Respond with success message
        except Todo.DoesNotExist:
            return Response({"message": "Todo not found or you don't have access to it."}, status=status.HTTP_404_NOT_FOUND)  # Handle case where todo does not exist or user doesn't own it

    def put(self, request, todo_id):
        """
        Updates a specific todo for the authenticated user.
        """
        try:
            todo = Todo.objects.get(id=todo_id, user=request.user)  # Get the todo item for the current user
            serializer = TodoSerializer(todo, data=request.data)  # Deserialize the input data
            print(serializer)
            if serializer.is_valid():  # Check if the input data is valid
                serializer.save()  # Save the updates to the database
                return Response(serializer.data, status=status.HTTP_200_OK)  # Respond with the updated todo data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Respond with validation errors
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found."}, status=status.HTTP_404_NOT_FOUND)