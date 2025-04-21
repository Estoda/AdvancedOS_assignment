from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TaskSerializer
from .models import Task
from django.utils.dateparse import parse_date

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        completed = self.request.query_params.get('completed')
        due_date = self.request.query_params.get('due_date')
        priority = self.request.query_params.get('priority')

        if completed is not None:
            queryset = queryset.filter(completed=completed.lower() == 'true')
        if due_date is not None:
            queryset = queryset.filter(due_date=parse_date(due_date))
        if priority is not None:
            queryset = queryset.filter(priority=priority.lower())
        
        return queryset
    
class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

@api_view(['PUT'])
def mark_completed(request, pk):
    task = Task.objects.get(pk=pk)
    task.completed = True
    task.save()
    return Response(TaskSerializer(task).data)

@api_view(['PUT'])
def mark_uncompleted(request, pk):
    task = Task.objects.get(pk=pk)
    task.completed = False
    task.save()
    return Response(TaskSerializer(task).data)

@api_view(['PUT'])
def update_priority(request, pk):
    task = Task.objects.get(pk=pk)
    priority = request.data.get('priority')
    if priority not in ['low', 'medium', 'high']:
        return Response({'error': 'Invalid priority'}, status=status.HTTP_400_BAD_REQUEST)
    task.priority = priority
    task.save()
    return Response(TaskSerializer(task).data)


