import docker


class Docker(object):
    """
    Basic class for docker operations,
    like a create, show and delete containers.
    """

    def __init__(self):
        self.docker_image = 'web-executor'
        self.client = docker.from_env()
        self.container = None

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
        Function return list of cantainer objects
        :return: [] containers
        """
        return self.client.containers.list(all=True)

    def start(self):
        """
        Create container.
        :return: dict, {'Id': string, 'Warnings': None or value}
        """
        self.container = self.client.containers.create(self.docker_image)
        return self.container_id

    def stop(self):
        """
        Stop container.
        :return:
        """
        return self.container.stop()

    def remove(self):
        """
        Remove container.
        :return:
        """
        return self.container.remove()
