from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TaskSerializer
from .models import Task
from django.utils.dateparse import parse_date
from django.shortcuts import render


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "priority"]
    ordering_fields = ["due_date", "priority"]

    def get_queryset(self):
        queryset = super().get_queryset()
        completed = self.request.query_params.get("completed")
        due_date = self.request.query_params.get("due_date")

        if completed is not None:
            queryset = queryset.filter(completed=completed)
        if due_date is not None:
            queryset = queryset.filter(due_date=due_date)

        return queryset


class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@api_view(["PUT"])
def mark_completed(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        task.completed = True
        task.save()
        return Response(
            {"message": "Task marked as completed"}, status=status.HTTP_200_OK
        )
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def mark_uncompleted(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        task.completed = False
        task.save()
        return Response(
            {"message": "Task marked as uncompleted"}, status=status.HTTP_200_OK
        )
    except task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def update_priority(request, pk):
    task = Task.objects.get(pk=pk)
    priority = request.data.get("priority")

    if priority not in ["low", "medium", "high"]:
        return Response(
            {"error": "Invalid priority. Please provide 'low', 'medium', or 'high'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    task.priority = priority
    task.save()
    return Response({"message": "Task priority updated"}, status=status.HTTP_200_OK)
