from rest_framework import serializers

from api.models import Task


class TaskSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    created = serializers.DateTimeField(required=False)

    class Meta:
        model = Task
        fields = ('pk', 'content', 'created')
