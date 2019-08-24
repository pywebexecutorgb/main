from django.urls import reverse_lazy, reverse
from rest_framework import serializers

from authapp.models import PyWebUser, PyWebUserProfile, UserCode
from mainapp.models import CodeBase, CodeExecution, Container


class CodeBaseSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()

    class Meta:
        model = CodeBase
        fields = ('pk', 'code_text', 'dependencies', 'created_at', 'url')
        lookup_field = 'pk'


class CodeExecutionSerializer(serializers.ModelSerializer):
    code = CodeBaseSerializer(read_only=True)

    class Meta:
        model = CodeExecution
        fields = ('code', 'has_errors', 'output', 'profile', 'processed_at')


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ('container_id', 'created_at', 'last_access_at')


class UserOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = PyWebUser
        exclude = ('is_superuser', 'is_active', 'is_staff', 'user_permissions',
                   'groups', 'date_joined', 'last_login', 'email', 'password')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PyWebUserProfile
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):
    pywebuserprofile = UserProfileSerializer(required=False, read_only=False)

    class Meta:
        model = PyWebUser
        extra_kwargs = {'password': {'write_only': True}}
        exclude = ('is_superuser', 'is_active', 'is_staff', 'user_permissions',
                   'groups', 'date_joined', 'last_login')

    def _pop_profile(self, validated_data):
        profile = validated_data.get('pywebuserprofile', {})
        if profile:
            # clean profile data if it's defined
            validated_data.pop('pywebuserprofile')
        return profile

    def create(self, validated_data):
        profile = self._pop_profile(validated_data)

        password = validated_data.pop('password')
        instance = PyWebUser.objects.create(**validated_data)
        instance.set_password(password)
        instance.save()

        profile.update({'user': instance})
        PyWebUserProfile.objects.create(**profile)
        return instance

    def update(self, instance, validated_data):
        profile = self._pop_profile(validated_data)
        PyWebUserProfile.objects.filter(user=instance).update(**profile)

        PyWebUser.objects.filter(pk=instance.pk).update(**{
            'username': validated_data.pop('username'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
        })

        return instance


class UserCodeSerializer(serializers.ModelSerializer):
    code = CodeBaseSerializer(required=False, read_only=True)

    class Meta:
        model = UserCode
        fields = ('user', 'code')
