from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from .util import Util

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'Complete':
            Util.send_update(self.request.user.email, instance.task_name)