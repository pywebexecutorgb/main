from django.utils import timezone
from datetime import timedelta

import mainapp.utils
from mainapp.models import CodeBase, CodeExecution, Container
from mainapp.utils import DockerExec, convert_output_to_profile, convert_error_to_profile, runtime_container_exec

from executor.celery import app


@app.task
def clean_containers():
    time = timezone.now() - timedelta(minutes=15)
    for container in Container.objects.filter(last_access_at__lte=time):
        print(container)
        try:
            docker_container = mainapp.utils.Container()
            docker_container.define(container.container_id)
            docker_container.remove()
        except Exception:
            pass
        container.delete()


def execute_code(code_id=None):
    """
    Function execute code from CodeBase by ID
    :param code_id: integer pk in CodeBase
    :return Model.save(): result
    """
    code = CodeBase.objects.get(pk=code_id)
    exec_output, exec_error = None, None
    try:
        with DockerExec(code.get_interpreter_display(),
                        code.code_text,
                        code.dependencies) as exec:
            exec_output, exec_error = exec.stdout, exec.stderr
    except Exception as err:
        exec_error = err

    if exec_error:
        c_exec = CodeExecution(code=code, has_errors=True, output=exec_error)
        return c_exec.save()

    (output, profile) = convert_output_to_profile(exec_output)
    c_exec = CodeExecution(code=code, has_errors=False,
                           output=output, profile=profile)
    return c_exec.save()


def execute_runtime_code(container_id, code, dependencies):
    exec_output, exec_error = None, None
    try:
        result_object = runtime_container_exec(container_id, code, dependencies)
        exec_output, exec_error = result_object.stdout, result_object.stderr
    except Exception as err:
        exec_error = err
    if exec_error:
        (error, _) = convert_error_to_profile(exec_error.decode('utf-8'))
        return {'has_errors': True, 'output': error}

    (output, profile) = convert_output_to_profile(exec_output.decode('utf-8'))
    return {'has_errors': False, 'output': output, 'profile': profile}
