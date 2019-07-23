from django.urls import reverse
from django.views.generic import DetailView, CreateView, RedirectView

from mainapp.forms import CodeBaseForm
from mainapp.models import CodeBase
from mainapp.utils import ShortURL


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


# This logic migrated into REST API: api/views.py
# def code_read_ajax(request, pk):
#     if request.is_ajax():
#         qs = get_object_or_404(CodeExecution, pk=pk)
#         return JsonResponse({'output': qs.output,
#                              'has_errors': qs.has_errors})


class ShortURLRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        link = self.kwargs.get('link')
        codebase_pk = ShortURL().decode(link)
        return reverse('code', kwargs={'pk': codebase_pk})
