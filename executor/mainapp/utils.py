"""
At the first you need to prepare init image:
$ docker build --tag web-executor-base --file Dockerfile .
from Dockerfile in root directory of the project!

How you can use it:

import mainapp.utils
tempdir = mainapp.utils.prepare_docker_exec('python3', 'print("OK")')
docker = mainapp.utils.Docker(tempdir)
docker.create()
    '8c3b628976a990222deefed8662e7eff09f506da02f6b48bbf5a3b8ed8f1ff98'
docker.start()
docker.container.container.logs()
    b'OK\n'

with DockerExec("python3", '''
import requests
try:
    print(requests.get("http://www.yandex.ru/").status_code)
except Exception as err:
    print(err)
''', "requests") as exec:
    print(exec.stdout, exec.stdout)
"""

import io
import os
import shutil
import string
import tarfile
import tempfile
import time
import types

from django.conf import settings

import jinja2
import docker
import short_url


def convert_output_to_profile(input=''):
    """
    Function split input text on output and profile result
    :param input: string, input text
    :return (output, profile output): string, string
    """
    if not input:
        return ("string doesn't defined", None)

    profile, output = [], []
    profile_starts_flag = False
    for line in input.split('\n'):
        if 'function calls' in line:
            profile_starts_flag = True
        if profile_starts_flag:
            profile.append(line)
            continue
        output.append(line)

    return ('\n'.join(output),
            '\n'.join(profile))


def prepare_docker_exec(python_interpreter='python3', script_data='', requirements_data=''):
    """
    Prepare working directory for running script with Dockerfile
    :param python_interpreter: string python or python3
    :param script_data: string with script value
    :param requirements_data: requirements.txt data
    :return directory path: string
    """
    workdir = tempfile.mkdtemp()

    try:
        use_pip = False
        if requirements_data:
            use_pip = True
            with open(os.path.join(workdir, 'requirements.txt'), 'w') as fh:
                fh.write(requirements_data)

        with open(os.path.join(workdir, 'exec.py'), 'w') as fh:
            fh.write(script_data)

        with open(os.path.join(workdir, 'Dockerfile'), 'w') as fh:
            fh_template = open(settings.DOCKERFILE_TEMPLATE, 'r')
            template = jinja2.Template(fh_template.read())
            fh.write(template.render(python_interpreter=python_interpreter,
                                     use_pip=use_pip))

    except Exception as e:
        shutil.rmtree(workdir)
        return None

    return workdir


def runtime_container_exec(container_id, script_data='', requirements_data=''):
    """
    Execute code in running container
    :param container_id: string
    :param script_data: string, that need to execute
    :param requirements_data: requirements.txt data
    :return object: with attrs "stdout" and "stderr"
    """
    return_obj = types.SimpleNamespace()
    return_obj.stdout = None
    return_obj.stderr = None

    container = Container()
    container.define(container_id)

    container.put(settings.DOCKER_TEMPORARY_DIRECTORY, 'requirements.txt', requirements_data)
    if requirements_data:
        container.put(settings.DOCKER_TEMPORARY_DIRECTORY, 'requirements.txt', requirements_data)
        container.exec(f'pip3 install --user -r {settings.DOCKER_TEMPORARY_DIRECTORY}/requirements.txt')

    container.put(settings.DOCKER_TEMPORARY_DIRECTORY, 'exec.py', script_data)
    (exit_code, output) = container.exec(f'python3 -u -m cProfile {settings.DOCKER_TEMPORARY_DIRECTORY}/exec.py')

    if exit_code == 0:
        return_obj.stdout = output
    else:
        return_obj.stderr = output

    return return_obj


class Container(object):
    @classmethod
    def _create_tar_io_stream(cls, filename, content):
        """
        Internal container method, that create IO stream for tar content,
        put_archive uses in to deploy data into container
        :param filename: string
        :param content: string
        :return tar_stream: BytesIO stream
        """
        tar_info = tarfile.TarInfo(name=filename)
        tar_info.size = len(content)
        tar_info.mtime = time.time()

        tar_stream = io.BytesIO()
        tar_file = tarfile.TarFile(fileobj=tar_stream, mode='w')
        tar_file.addfile(tarinfo=tar_info, fileobj=io.BytesIO(content.encode('utf-8')))
        tar_file.close()

        tar_stream.seek(0)
        return tar_stream

    def __init__(self, image_id=None):
        self.image_id = image_id
        self.container = None

        self.client = docker.from_env()

    @property
    def container_id(self):
        return self.container.id

    def define(self, container_id):
        """
        Get container by ID.
        :param container_id: string
        :return container id: string
        """
        self.container = self.client.containers.get(container_id)
        return self

    def run(self):
        """
        Run container (like a "create" and "start")
        :return container id: string
        """
        self.container = self.client.containers.run(self.image_id, detach=True,
                                                    stdout=True, stderr=True)
        return self.container_id

    def create(self):
        """
        Start container.
        :return container id: string
        """

        self.container = self.client.containers.create(self.image_id)
        return self.container_id

    def start(self):
        """
        Start container.
        :return None: None
        """
        return self.container.start()

    def stop(self):
        """
        Stop container.
        :return None: None
        """
        return self.container.stop()

    def remove(self):
        """
        Remove container.
        :return None: None
        """
        return self.container.remove(force=True)

    def put(self, directory, filename, content):
        """
        Put archive files into container.
        :param directory: string
        :param filename: string
        :param content: bytes
        :return result of put_archive operation: bool, true if the call succeeds
        """
        tar_stream = Container._create_tar_io_stream(filename, content)
        return self.container.put_archive(directory, tar_stream)

    def exec(self, cmd):
        """
        Execute command into container
        :param cmd: string
        :return (exit_code, output): result of exec_run operation
        """
        return self.container.exec_run(cmd)


class Docker(Container):
    """
    Basic class for docker operations,
    like a create, show and delete containers.
    """

    def __init__(self, dockerfile_dirpath):
        self.client = docker.from_env()
        self.docker_image, self.build_logs = self._build_image(dockerfile_dirpath)

        self.container = None

    def destroy(self):
        try:
            self.container.remove()
        except Exception:
            pass

        return self._remove_image()

    @property
    def image_id(self):
        """
        :return string: created image ID (after __init__ call) or None
        """
        if hasattr(self.docker_image, 'id'):
            return self.docker_image.id
        return None

    @property
    def containers(self):
        """
        Function return list of cantainers objects
        :return containers: []
        """
        return self.client.containers.list(all=True)

    def _build_image(self, dockerfile_dirpath):
        """
        Create docker from Dockerfile in input directory
        :param dockerfile_dirpath: string - directory path to Dockerfile
        :return [images object, JSON logs]:
        """
        return self.client.images.build(path=dockerfile_dirpath, forcerm=True)

    def _remove_image(self):
        """
        Force remove image with based ID
        :return None: None
        """
        try:
            return self.client.images.remove(image=self.image_id, force=True)
        except Exception:
            pass
        return False

    def create(self):
        """
        Create container.
        :return {'Id': string, 'Warnings': None or value}: dict
        """
        self.container = Container(self.image_id)
        self.container.create()
        return self.container.container_id

    def run(self):
        """
        Run container. Using in DockerExec class as the simplest method for run docker.
        :return logs: string
        """
        self.container = Container(self.image_id)
        self.container.run()

        # back compatibility magic: DockerExec use wait operation for internal
        return self.container.container


class DockerExec(object):
    """
    Class that allow simple access to run python script:
        with DockerExec("python3", '''
            import requests
            try:
                print(requests.get("http://www.yandex.ru/").status_code)
            except Exception as err:
                print(err)
            ''', "requests") as exec:
                for msg in exec:
                    print(msg)
    """

    def __init__(self, python_interpreter='python3',
                 script_data='', requirements_data=''):
        """
        Init function of DockerExec
        :param python_interpreter: string 'python' or 'python3'
        :param script_data: string with python code
        :param requirements_data: string with requirements.txt content
        """
        self.script_data = script_data
        self.requirements_data = requirements_data
        self.python_interpreter = python_interpreter

        self.workdir = None
        self.client = None
        self.container = None

    def __enter__(self):
        """
        Enter function initialize container and run script.
        :return object: with attrs "stdout" and "stderr"
        """
        return_obj = types.SimpleNamespace()
        return_obj.stdout = None
        return_obj.stderr = None

        self.workdir = prepare_docker_exec(self.python_interpreter,
                                           self.script_data,
                                           self.requirements_data)

        self.client = Docker(self.workdir)
        try:
            container = self.client.run()
            container.wait(timeout=60)
        except Exception as err:
            return_obj.stderr = str(err)
            return return_obj

        return_obj.stdout = container.logs(stdout=True, stderr=False).decode('utf-8')
        return_obj.stderr = container.logs(stdout=False, stderr=True).decode('utf-8')
        return return_obj

    def __exit__(self, *args):
        """
        Function remove all objects
        :return None: None
        """
        self.client.destroy()
        shutil.rmtree(self.workdir)


class ShortURL(object):
    """
    Convert string to long or short presentation.
        short_cls = ShortURL()
        short_cls.encode(1234567890)
'           bvIhFu'
        short_cls.decode('bvIhFu')
            1234567890
    """

    def __init__(self):
        """
        Init base variable short_url.
        """
        self.short_url = short_url.UrlEncoder(alphabet=
                                              string.ascii_lowercase +
                                              string.ascii_uppercase +
                                              '0123456789',
                                              block_size=0)

    def encode(self, value):
        """
        Return short form of input interger value
        :param value: interger ID
        :return shortened URL: string
        """
        return self.short_url.encode_url(value)

    def decode(self, value):
        """
        Return long form of input string value
        :param value: string URL
        :return integer: source integer value
        """
        return self.short_url.decode_url(value)
