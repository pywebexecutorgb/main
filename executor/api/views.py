from datetime import datetime

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import CodeBaseSerializer, CodeExecutionSerializer, ContainerSerializer
from mainapp.models import CodeBase, CodeExecution, Container
from mainapp.tasks import execute_runtime_code

import mainapp.utils


class CodeBaseSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = CodeBase.objects.all()
    serializer_class = CodeBaseSerializer
    # http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        obj = super(CodeBaseSet, self).create(request, *args, **kwargs)
        if obj.data.get('pk') is None:
            raise RuntimeError("ID is not defined")

        return HttpResponseRedirect(redirect_to=reverse('api:codeexecution-detail',
                                                        kwargs={'pk': obj.data.get('pk')}))


class CodeExecutionSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = CodeExecution.objects.all()
    serializer_class = CodeExecutionSerializer
    # http_method_names = ['get']

    def retrieve(self, request, pk):
        queryset = CodeExecution.objects.select_related('code').all()

        data = get_object_or_404(queryset, code__pk=pk)
        serializer = CodeExecutionSerializer(data)

        return Response(serializer.data)


class ContainerSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def codes(self, request, pk):
        serializer = CodeBaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        json_result = execute_runtime_code(pk, request.data['code_text'], request.data['dependencies'])
        return JsonResponse(json_result)

    def retrieve(self, request, pk):
        queryset = Container.objects.all()
        data = get_object_or_404(queryset, container_id=pk)
        serializer = ContainerSerializer(data)

        return Response(serializer.data)

    def update(self, request, pk):
        datetime_value = datetime.fromtimestamp(request.data.get('date', 0) / (10 ** 3))

        queryset = Container.objects.filter(container_id=pk)
        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)

        queryset.update(last_access_at=make_aware(datetime_value))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        try:
            container = mainapp.utils.Container()
            container.define(pk)
            container.stop()
            container.remove()
        except Exception:
            pass

        Container.objects.filter(container_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
