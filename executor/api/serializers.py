from django.urls import reverse_lazy
from rest_framework import serializers

from mainapp.models import CodeBase, CodeExecution


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
