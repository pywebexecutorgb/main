"""
for creating a superuser, run the commands via 'python manage.py shell':
> from authapp.models import PyWebUser
> super_user = PyWebUser.objects.create_superuser('admin', 'admin@pwe.local', 'admin', age=20)
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from mainapp.models import CodeBase


class PyWebUser(AbstractUser):
    username = models.CharField(verbose_name="username", max_length=128, unique=True)
    email = models.EmailField(verbose_name="email", unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class PyWebUserProfile(models.Model):
    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    user = models.OneToOneField(PyWebUser, on_delete=models.CASCADE)
    userphoto = models.ImageField(upload_to='userphotos', blank=True)
    age = models.PositiveIntegerField(verbose_name='age', null=True, blank=True, validators=[MaxValueValidator(100),
                                                                                             MinValueValidator(1)])
    gender = models.CharField(verbose_name='gender', max_length=1, choices=GENDER_CHOICES, blank=True)
    country = models.CharField(verbose_name='country', max_length=128, blank=True)
    state = models.CharField(verbose_name='state', max_length=128, blank=True)
    city = models.CharField(verbose_name='city', max_length=128, blank=True)
    zipcode = models.CharField(verbose_name='zipcode', max_length=16, blank=True)
    company = models.CharField(verbose_name='company', max_length=256, blank=True)
    bio = models.TextField(verbose_name='bio', max_length=2048, blank=True)
    socials = models.CharField(verbose_name='socials', max_length=512, blank=True)
    proglangs = models.CharField(verbose_name='programming languages', max_length=512, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class UserCode(models.Model):
    class Meta:
        unique_together = ('user', 'code')
        verbose_name = "User's Code"
        verbose_name_plural = "User's Codes"

    user = models.ForeignKey(PyWebUser, on_delete=models.CASCADE)
    code = models.ForeignKey(CodeBase, on_delete=models.CASCADE)
