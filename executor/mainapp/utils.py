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
docker.container.logs()
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

import os
import shutil
import string
import tempfile
import types

from django.conf import settings
# from django.template.loader import render_to_string

import jinja2
import docker
import short_url


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
            # Use jinja2 templates instead django:
            # fh.write(render_to_string(settings.DOCKERFILE_TEMPLATE,
            #                           {'python_interpreter': python_interpreter,
            #                            'use_pip': use_pip}))
            fh_template = open(settings.DOCKERFILE_TEMPLATE, 'r')
            template = jinja2.Template(fh_template.read())
            fh.write(template.render(python_interpreter=python_interpreter,
                                     use_pip=use_pip))

    except Exception as e:
        shutil.rmtree(workdir)
        return None

    return workdir


class Docker(object):
    """
    Basic class for docker operations,
    like a create, show and delete containers.
    """

    def __init__(self, dockerfile_dirpath):
        self.client = docker.from_env()
        self.docker_image, self.build_logs = self._build_image(dockerfile_dirpath)

        self.container = None

    def __del__(self):
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
    def container_id(self):
        """
        :return container ID or None: string or None
        """
        if hasattr(self.container, 'id'):
            return self.container.id
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
        return self.client.images.remove(image=self.image_id, force=True)

    def create(self):
        """
        Create container.
        :return {'Id': string, 'Warnings': None or value}: dict
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

    def run(self):
        """
        Run container. Using in DockerExec class as the simplest method for run docker.
        :return logs: string
        """
        self.container = self.client.containers.run(self.image_id, detach=True,
                                                    stdout=True, stderr=True)
        return self.container


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
        del self.client
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
