from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user', 'task_name', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_status(self, value):
        if value not in ['Incomplete', 'Complete']:
            raise serializers.ValidationError("Status must be either 'Incomplete' or 'Complete'")
        return value