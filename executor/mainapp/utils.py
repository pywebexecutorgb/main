"""
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
import tempfile

from django.conf import settings

import jinja2
import docker


def prepare_docker_exec(script_data='', requirements_data='', python_interpreter='python3'):
    """
    Prepare working directory for running script with Dockerfile
    :param script_data: string with script value
    :param requirements_data: requirements.txt data
    :param python_interpreter: string python or python3
    :return string: directory path
    """
    workdir = tempfile.mkdtemp()

    try:
        with open(os.path.join(workdir, 'requirements.txt'), 'w') as fh:
            fh.write(requirements_data)
        with open(os.path.join(workdir, 'exec.py'), 'w') as fh:
            fh.write(script_data)
        with open(os.path.join(workdir, 'Dockerfile'), 'w') as fh:
            template = jinja2.Template(open(settings.DOCKERFILE_TEMPLATE, 'r').read())
            fh.write(template.render(local_directory=workdir,
                                     python_interpreter=python_interpreter))
    except Exception as e:
        os.unlink(workdir)
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
        :return: string, created container ID (after start call) or None
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
        return self.client.images.build(path=dockerfile_dirpath)

    def _remove_image(self):
        """
        Force remove image with based ID
        :return: None
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
        :return: None
        """
        return self.container.start()

    def stop(self):
        """
        Stop container.
        :return None:
        """
        return self.container.stop()

    def remove(self):
        """
        Remove container.
        :return None:
        """
        return self.container.remove()
