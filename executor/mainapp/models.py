'''
> output, profile = [], []
> command = """
> import requests
> try:
>     print(requests.get("http://www.yandex.ru/").status_code)
> except Exception as err:
>     print(err)
> """

> from mainapp.utils import DockerExec
> with DockerExec('python3', command, "requests") as exec:
>     profile_flag = False
>     for msg in exec:
>         if 'function calls' in msg:
>             profile_flag = True
>         if profile_flag:
>             profile.append(msg)
>             continue
>         output.append(msg)
>         print(msg)
    200

> from mainapp.models import CodeBase, CodeExecution
> codebase = CodeBase(code_text=command)
> codebase.save()
> codebase
    <CodeBase: 1 (
    import requests
    try:
        print(, False)>

> code_exec = CodeExecution(code=codebase, output='\n'.join(output), profile='\n'.join(profile))
> code_exec.save()
> code_exec
    <CodeExecution: 1 (
    import requests
    try:
        print(, 200,          190125 function calls ()>
'''

from django.db import models


class CodeBase(models.Model):
    class Meta:
        verbose_name = "User's code"
        verbose_name_plural = "User's code"

    code_text = models.CharField(verbose_name='Code text', max_length=2048)
    is_errors = models.BooleanField(verbose_name='Errors', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return f"{self.pk} ({self.code_text[:32]}, {self.is_errors})"


class CodeExecution(models.Model):
    class Meta:
        verbose_name = "User's code result"
        verbose_name_plural = "User's code results"

    code = models.ForeignKey(CodeBase, related_name='code', on_delete=models.CASCADE)
    output = models.CharField(verbose_name='Code execution result', max_length=2048)
    profile = models.CharField(verbose_name='Code profile result', max_length=2048)

    def __str__(self):
        return f"{self.pk} ({self.code.code_text[:32]}, {self.output[:32]}, {self.profile[:32]})"
