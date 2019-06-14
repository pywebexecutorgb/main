"""
At the first you need to prepare init image:
$ docker build --tag web-executor-base --file Dockerfile .
from Dockerfile in root directory of the project!

How you can use it:

> import mainapp.utils
> tempdir = mainapp.utils.prepare_docker_exec('print("OK")')
> docker = mainapp.utils.Docker(tempdir)
> docker.create()
'8c3b628976a990222deefed8662e7eff09f506da02f6b48bbf5a3b8ed8f1ff98'
> docker.start()
> docker.container.logs()
b'OK\n'
"""

# TODO: clean temporary directory

import os
import shutil
import tempfile

from django.conf import settings

import jinja2
import docker


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
            with open(os.path.join(workdir, 'requirements.txt'), 'w') as fh:
                fh.write(requirements_data)
            use_pip = True

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
        return self.client.containers.run(self.image_id, auto_remove=True)


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

    def __enter__(self):
        """
        Enter function initialize container and run script.
        :return yield logs: [strings]
        """
        self.workdir = prepare_docker_exec(self.python_interpreter,
                                           self.script_data,
                                           self.requirements_data)
        self.client = Docker(self.workdir)
        logs = self.client.run()
        for line in logs.decode('utf-8').split('\n'):
            yield line

    def __exit__(self, *args):
        """
        Function remove all objects
        :return None: None
        """
        del self.client
        shutil.rmtree(self.workdir)
