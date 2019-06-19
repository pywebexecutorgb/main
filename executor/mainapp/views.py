from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, CreateView

from mainapp.forms import CodeBaseForm
from mainapp.models import CodeBase, CodeExecution


class CodeCreate(CreateView):
    model = CodeBase
    form_class = CodeBaseForm

    def get_success_url(self):
        return reverse('mainapp:read', args=(self.object.pk,))


class CodeRead(DetailView):
    model = CodeBase

    def get_queryset(self):
        return CodeBase.objects.select_related(
            'codeexecution'
        ).filter(pk=self.kwargs.get('pk'))
