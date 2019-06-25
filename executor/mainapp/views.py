from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView
from .forms import CodeBaseForm
from .utils import DockerExec
from .models import CodeBase, CodeExecution


project_title = 'WebExecutor'

activity_buttons = [
    {
        'href': 'index', 'name': 'run'
    },
    {
        'href': 'index', 'name': 'save'
    },
    {
        'href': 'index', 'name': 'new'
    },
]


class CodeCreate(CreateView):
    model = CodeBase
    form_class = CodeBaseForm
    template_name = 'mainapp/index.html'
    success_url = reverse_lazy('mainapp:read')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create | ' + project_title
        context['activity_buttons'] = activity_buttons
        return context


class CodeRead(DetailView):
    model = CodeExecution
    template_name = 'mainapp/code_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Read | ' + project_title
        context['code_execution'] = 'Read | ' + project_title
        return context

    # def get_queryset(self):
        # return CodeBase.objects.select_related('codebase').filter(pk=self.kwargs.get('pk'))


# def code_execution(request, pk):
#     output, profile = [], []
#     code_exec = None
#     with DockerExec(CodeBase.get_interpreter_display(), CodeBase.code_text, CodeBase.dependencies) as exec:
#         if exec.stderr:
#             code_exec = CodeExecution(code=CodeBase, has_errors=True, output=exec.stderr, profile='')
#         else:
#             profile_flag = False
#             for line in exec.stdout.split('\n'):
#                 if 'function calls' in line:
#                     profile_flag = True
#                 if profile_flag:
#                     profile.append(line)
#                     continue
#                 output.append(line)
#             code_exec = CodeExecution(code=CodeBase,
#                                       has_errors=False,
#                                       output='\n'.join(output),
#                                       profile='\n'.join(profile))
#         code_exec.save()


# activity_buttons = [
#     {
#         'href': 'index', 'name': 'run'
#     },
#     {
#         'href': 'index', 'name': 'save'
#     },
#     {
#         'href': 'index', 'name': 'new'
#     },
# ]

# def main(request):
#     title = 'WebExecutor'
#     content = {
#         'title': title,
#         'activity_buttons': activity_buttons,
#     }
#
#     return render(request, 'mainapp/index.html', content)
