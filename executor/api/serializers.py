from django.urls import reverse_lazy, reverse
from rest_framework import serializers

from mainapp.models import CodeBase, CodeExecution, Container


class CodeBaseSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()

    class Meta:
        model = CodeBase
        fields = ('pk', 'code_text', 'dependencies', 'created_at', 'url')
        lookup_field = 'pk'


class CodeExecutionSerializer(serializers.ModelSerializer):
    code = CodeBaseSerializer(read_only=True)

    class Meta:
        model = CodeExecution
        fields = ('code', 'has_errors', 'output', 'profile', 'processed_at')


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ('container_id', 'created_at', 'last_access_at')
