from hashlib import sha3_512

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView

from mainapp.forms import CodeBaseForm
from mainapp.models import CodeBase


class CodeCreate(CreateView):
    model = CodeBase
    form_class = CodeBaseForm

    def get_success_url(self):
        return reverse('mainapp:read', args=(self.object.pk,))

    def form_valid(self, form):
        """
        Validate that executable code doesn't exist
        :param form: django form object
        :return: redirect on exists code or make form_valid()
        """
        hash_digest = sha3_512(form.instance.code_text.encode('utf-8') +
                               form.instance.dependencies.encode('utf-8')).hexdigest()
        object_by_hash = CodeBase.has_digest(hash_digest)
        if object_by_hash:
            return HttpResponseRedirect(reverse('mainapp:read', args=(object_by_hash.pk,)))
        return super(CodeCreate, self).form_valid(form)


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
