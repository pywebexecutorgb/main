from datetime import datetime

from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.serializers import CodeBaseSerializer, CodeExecutionSerializer, ContainerSerializer, \
    UserSerializer, UserProfileSerializer, UserOnlySerializer, UserCodeSerializer
from authapp.models import PyWebUser, PyWebUserProfile, UserCode
from authapp.utils import TokenGenerator, send_user_email
from mainapp.models import CodeBase, CodeExecution, Container
from mainapp.tasks import execute_runtime_code
import mainapp.utils


class CodeBaseSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = CodeBase.objects.all()
    serializer_class = CodeBaseSerializer

    # http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        obj = super(CodeBaseSet, self).create(request, *args, **kwargs)
        if obj.data.get('pk') is None:
            raise RuntimeError("ID is not defined")
        if request.user.is_authenticated:
            try:
                UserCode(user_id=request.user.pk,
                         code_id=obj.data.get('pk')).save()
            except Exception:
                # here we can caught exception,
                # when user try to save already exist code
                pass

        return HttpResponseRedirect(redirect_to=reverse('api:codeexecution-detail',
                                                        kwargs={'pk': obj.data.get('pk')}))


class CodeExecutionSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = CodeExecution.objects.all()
    serializer_class = CodeExecutionSerializer

    # http_method_names = ['get']

    def retrieve(self, request, pk):
        queryset = CodeExecution.objects.select_related('code').all()

        data = get_object_or_404(queryset, code__pk=pk)
        serializer = CodeExecutionSerializer(data)

        return Response(serializer.data)


class ContainerSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def codes(self, request, pk):
        serializer = CodeBaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        json_result = execute_runtime_code(pk, request.data['code_text'], request.data['dependencies'])
        return JsonResponse(json_result)

    def retrieve(self, request, pk):
        queryset = Container.objects.all()
        data = get_object_or_404(queryset, container_id=pk)
        serializer = ContainerSerializer(data)

        return Response(serializer.data)

    def update(self, request, pk):
        datetime_value = datetime.fromtimestamp(request.data.get('date', 0) / (10 ** 3))

        queryset = Container.objects.filter(container_id=pk)
        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)

        queryset.update(last_access_at=make_aware(datetime_value))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        try:
            container = mainapp.utils.Container()
            container.define(pk)
            container.stop()
            container.remove()
        except Exception:
            pass

        Container.objects.filter(container_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSet(viewsets.ModelViewSet):
    queryset = PyWebUser.objects.select_related('pywebuserprofile').all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """
        Function display only current user, not full list,
        like a retrieve, but without "pk" argument.
        :return JSON: string with object or error message
        """
        if request.user.is_authenticated:
            user_object = get_object_or_404(UserSet.queryset, pk=request.user.pk)
            return JsonResponse(UserSerializer(user_object).data, status=status.HTTP_200_OK)

        return JsonResponse(data={'error': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk):
        """
        Function display only current user, if you send
        of other user you see 403 forbidden.
        :return JSON: string with object or error message
        """
        if not request.user.is_authenticated or request.user.pk != int(pk):
            return JsonResponse(data={'error': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        data = get_object_or_404(UserSet.queryset, pk=pk)
        serializer = UserSerializer(data)

        return JsonResponse(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create user.
        It's include user and profile data.
        If profile is empty, it will be created too.
        :return JSON: serialized object data
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # send verification email, when create user
            user_object = PyWebUser.objects.get(pk=serializer.data.get('id'))
            send_user_email(request, user_object, 'validate-email')

            return JsonResponse({'id': serializer.data.get('id')}, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """
        Update current user data.
        It's include user and profile data without mail and password,
        because if mail changed need to revalidate it — more logic, more problems.
        :return JSON: serialized object data
        """
        if not request.user.is_authenticated or request.user.pk != int(pk):
            return JsonResponse(data={'error': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data)

    def destroy(self, request, pk):
        """
        Delete user by this user.
        If other user try to delete not the same, forbidden will be returned.
        :return Dict: empty dict {} and status code 204.
        """
        if not request.user.is_authenticated or request.user.pk != int(pk):
            return Response(status=status.HTTP_403_FORBIDDEN)

        UserSet.queryset.filter(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCodeSet(mixins.ListModelMixin, GenericViewSet):
    class StandardPaginationSet(PageNumberPagination):
        page_size = 4
        max_page_size = 1000

    queryset = UserCode.objects.select_related('code').order_by('-code__pk')
    serializer_class = UserCodeSerializer
    pagination_class = StandardPaginationSet
    # permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return UserCodeSet.queryset.none()
        return UserCodeSet.queryset.filter(user_id=user.pk)


class ProfileView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_profile_form.html'

    def get(self, request, format=None, *args, **kwargs):
        user = get_object_or_404(PyWebUser, pk=request.user.pk)
        profile = UserOnlySerializer(user)

        user_profile = get_object_or_404(PyWebUserProfile, user=request.user.pk)
        extended_profile = UserProfileSerializer(user_profile)

        return Response({'user': user, 'profile': profile,
                         'extended_profile': extended_profile})

    def post(self, request, format=None, *args, **kwargs):
        user = get_object_or_404(PyWebUser, pk=request.user.pk)
        profile = UserOnlySerializer(user, data=request.data)
        if not profile.is_valid():
            return JsonResponse({'error': 'Update base profile failed'},
                                status=status.HTTP_400_BAD_REQUEST)
        profile.save()

        user_profile = get_object_or_404(PyWebUserProfile, user=request.user.pk)
        extended_profile = UserProfileSerializer(user_profile, data=request.data)
        if not extended_profile.is_valid():
            return JsonResponse({'error': 'Update exteneded profile failed'},
                                status=status.HTTP_400_BAD_REQUEST)
        extended_profile.save()

        return JsonResponse({'status': 'updated'}, status=status.HTTP_200_OK)


class AuthView(APIView):
    def delete(self, request, format=None, *args, **kwargs):
        """
        Function logout user on DELETE request to auth URL.
        :return status_code: 204 - successful, 400 - error.
        """
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None, *args, **kwargs):
        """
        Authorize user with POST request.
        :return status_code: 204 - successful, 400 - error.
        """
        user = authenticate(email=request.data.get('email'),
                            password=request.data.get('password'))
        if not user or not user.is_active:
            return JsonResponse({'error': 'user does not exist or inactive'},
                                status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ValidateEmailView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        """
        Check email validation and activate account with GET request
        :return status_code: 200 - successful, 400 - error.
        """
        result, user = TokenGenerator().is_token_valid(kwargs.get('uid'), kwargs.get('token'))
        if result:
            user.is_active = True
            user.save()
            login(request, user)
            return JsonResponse({'result': 'verified'}, status=status.HTTP_200_OK)

        return JsonResponse({'error': 'token is incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, format=None, *args, **kwargs):
        """
        Reset password user with POST request.
        :return status_code: 204 - successful, 400 - error.
        """

        def _request_password_reset(request):
            """
            Function send email with reset-password link.
            :param request: waiting for 'email' in data
            :return: JsonResponse object and status code: 200 - ok, 400 - error
            """
            user = UserSet.queryset.filter(email=request.data.get('email')).first()
            if not user or not user.is_active:
                return JsonResponse({'error': 'user does not exist or inactive'},
                                    status=status.HTTP_400_BAD_REQUEST)

            result = send_user_email(request, user, 'reset-password')
            return JsonResponse({'result': result}, status=status.HTTP_200_OK)

        def _execute_password_reset(request, uid, token):
            """
            Function check user token and reset password.
            :param request: waiting for 'password' in data
            :param uid: uid string
            :param token: token string
            :return: JSONResponse object and status code: 200 - ok, 400 - error
            """
            result, user = TokenGenerator().is_token_valid(uid, token)
            if not result:
                return JsonResponse({'error': 'token is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(request.data.get('password', None))
            user.save()
            return JsonResponse({'result': 'password has updated'}, status=status.HTTP_200_OK)

        # main logic: check exists uid and token, if true - reset, false - send reset link
        uid, token = kwargs.get('uid', None), kwargs.get('token', None)
        if uid is not None and token is not None:
            return _execute_password_reset(request, uid, token)

        return _request_password_reset(request)


class ShortURLView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        """
        Function receive hash and convert in into record ID in Code model.
        If code ID is incorrect, 404 will be returned.
        :param kwargs: dict, get value by 'hash' jey
        :return JSON or 404: {'code_id'}
        """
        code_id = mainapp.utils.ShortURL().decode(kwargs.get('hash', 0))
        get_object_or_404(CodeBaseSet.queryset, pk=code_id)

        return JsonResponse({'code_id': code_id})
