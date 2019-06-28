'''
How to try execute code and store it:

from mainapp.models import CodeBase, CodeExecution
from mainapp.utils import DockerExec
codebase = CodeBase(interpreter=CodeBase.INTERPRETER_PYTHON3, code_text="""
import requests
try:
    print(requests.get("http://www.yandex.ru/").status_code)
except Exception as err:
    print(err)
""", dependencies="requests")
output, profile = [], []
codebase.save()

code_exec = None
with DockerExec(codebase.get_interpreter_display(), codebase.code_text, codebase.dependencies) as exec:
    if exec.stderr:
        code_exec = CodeExecution(code=codebase, has_errors=True, output=exec.stderr, profile='')
    else:
        profile_flag = False
        for line in exec.stdout.split('\n'):
            if 'function calls' in line:
                profile_flag = True
            if profile_flag:
                profile.append(line)
                continue
            output.append(line)
        code_exec = CodeExecution(code=codebase, has_errors=False, output='\n'.join(output), profile='\n'.join(profile))
    code_exec.save()

codebase
    <CodeBase: 1
                    interpreter='python3'
                    code='
    import requests
    try:
        print(requests.get("http://www.yandex.'
                    dependencies='requests'>

code_exec
    <CodeExecution: 4:
                    code='
    import requests
    try:
        print(',
                    has_errors='False'
                    output='200',
                    profile='         190188 function calls ('>
'''

from hashlib import sha3_512

from django.db import models


class CodeBase(models.Model):
    INTERPRETER_PYTHON2 = 2
    INTERPRETER_PYTHON3 = 3

    INTERPRETER_CHOICES = (
        (INTERPRETER_PYTHON2, 'python'),
        (INTERPRETER_PYTHON3, 'python3'),
    )

    class Meta:
        verbose_name = "User's code"
        verbose_name_plural = "User's code"

    interpreter = models.PositiveSmallIntegerField(verbose_name='Python interpreter version',
                                                   choices=INTERPRETER_CHOICES,
                                                   default=INTERPRETER_PYTHON3)
    code_text = models.CharField(verbose_name='Code text', max_length=2048)
    dependencies = models.CharField(verbose_name='requirements.txt', max_length=256,
                                    blank=True, default='')
    hash_digest = models.CharField(verbose_name='SHA-512 digest of code text', max_length=128,
                                   null=True, blank=True, default=None, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""{self.pk}
                interpreter='{self.get_interpreter_display()}'
                code='{self.code_text[:64]}'
                dependencies='{self.dependencies}'"""

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Digest doesn't include python, because python2 is deprecated
        and we don't allow use it.
        """
        self.hash_digest = sha3_512(self.code_text.encode('utf-8') +
                                    self.dependencies.encode('utf-8')).hexdigest()

        is_code_exist = CodeBase.has_digest(self.hash_digest)
        if is_code_exist:
            self.id = is_code_exist.pk
            return

        return super(CodeBase, self).save()

    @classmethod
    def has_digest(cls, digest=None):
        return cls.objects.filter(hash_digest=digest).first()


class CodeExecution(models.Model):
    class Meta:
        verbose_name = "User's code result"
        verbose_name_plural = "User's code results"

    code = models.OneToOneField(CodeBase, on_delete=models.CASCADE, primary_key=True)
    processed_at = models.DateTimeField(verbose_name='Execution timestamp', auto_now_add=True)
    has_errors = models.BooleanField(verbose_name='Does code have errors?', default=False)

    output = models.CharField(verbose_name='Code execution result', max_length=2048)
    profile = models.CharField(verbose_name='Code profile result', max_length=2048,
                               null=True, default=None)

    def __str__(self):
        return f"""{self.pk}:
                code='{self.code.code_text[:32]}',
                has_errors='{self.has_errors}'
                output='{self.output[:32]}'"""
