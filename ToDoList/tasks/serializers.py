from rest_framework import serializers
from .models import Task
from django.utils.timezone import now


class TaskSerializer(serializers.ModelSerializer):

    def validate_due_date(self, value):
        if value and value.date() < now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate_priority(self, value):
        if value not in [1, 2, 3]:
            raise serializers.ValidationError(
                "Priority must be one of 'low', 'medium', or 'high'."
            )
        return value

    class Meta:
        model = Task
        fields = "__all__"
