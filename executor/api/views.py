# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import CodeBaseSerializer, CodeExecutionSerializer
from mainapp.models import CodeBase, CodeExecution


class CodeBaseSet(viewsets.ModelViewSet):
    queryset = CodeBase.objects.all()
    serializer_class = CodeBaseSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        obj = super(CodeBaseSet, self).create(request, *args, **kwargs)
        if obj.data.get('pk') is None:
            raise RuntimeError("ID is not defined")

        return HttpResponseRedirect(redirect_to=reverse('api:codeexecution-detail',
                                                        kwargs={'pk': obj.data.get('pk')}))


class CodeExecutionSet(viewsets.ModelViewSet):
    queryset = CodeExecution.objects.all()
    serializer_class = CodeExecutionSerializer
    http_method_names = ['get']

    def retrieve(self, request, pk=None):
        queryset = CodeExecution.objects.select_related('code').all()

        data = get_object_or_404(queryset, code__pk=pk)
        serializer = CodeExecutionSerializer(data)

        return Response(serializer.data)
