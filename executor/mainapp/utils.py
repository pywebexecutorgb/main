import docker


class Docker(object):
    """
    Basic class for docker operations,
    like a create, show and delete containers.
    """

    def __init__(self):
        self.docker_image = 'web-executor'
        self.client = docker.from_env()
        self.container = {}

    @property
    def container_id(self):
        """
        :return: string, created container ID (after start call) or None
        """
        return self.container.get('Id', None)

    def start(self):
        """
        Create container.
        :return: dict, {'Id': string, 'Warnings': None or value}
        """
        self.container = self.client.create_container(self.docker_image, detach=True)
        return self.container_id

    def stop(self):
        return self.client.remove_container(self.container_id)

    def list(self):
        return self.client.containers()
