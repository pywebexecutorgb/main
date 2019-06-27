from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, CreateView

from mainapp.forms import CodeBaseForm
from mainapp.models import CodeBase, CodeExecution


class CodeCreate(CreateView):
    model = CodeBase
    form_class = CodeBaseForm

    def get_success_url(self):
        if self.request.is_ajax():
            return reverse('mainapp:ajax_read', args=(self.object.pk,))

        return reverse('mainapp:read', args=(self.object.pk,))


class CodeRead(DetailView):
    model = CodeBase
    template_name = 'mainapp/codebase_form.html'

    def get_queryset(self):
        return CodeBase.objects.select_related(
            'codeexecution'
        ).filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(CodeRead, self).get_context_data(**kwargs)

        form = CodeBaseForm(initial={
            'interpreter': self.object.interpreter,
            'code_text': self.object.code_text,
            'dependencies': self.object.dependencies})
        context.update({'form': form})

        return context

def code_read_ajax(request, pk):
    if request.is_ajax():
        qs = get_object_or_404(CodeExecution, pk=pk)
        return JsonResponse({'output': qs.output,
                             'has_errors': qs.has_errors})