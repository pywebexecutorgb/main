import docker


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

    def start(self):
        """
        Create container.
        :return {'Id': string, 'Warnings': None or value}: dict
        """
        self.container = self.client.containers.create(self.image_id)
        return self.container_id

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
