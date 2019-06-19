from django.dispatch import receiver
from django.db.models.signals import post_save

from mainapp.models import CodeBase
from mainapp.tasks import execute_code


@receiver(post_save, sender=CodeBase)
def post_save_create_code_base(sender, instance, **kwargs):
    """
    Signal, that activate code execution in Docker.
    :param sender, instance, kwargs: default input params of receiver signal
    :return Model.save(): result
    """
    if not instance.pk:
        return None
    return execute_code(instance.pk)
