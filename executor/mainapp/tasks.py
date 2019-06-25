from mainapp.models import CodeBase, CodeExecution
from mainapp.utils import DockerExec, convert_output_to_profile


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
