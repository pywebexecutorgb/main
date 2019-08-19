from django.urls import path, include
from rest_framework import routers

from api.views import CodeBaseSet, CodeExecutionSet, ContainerSet, UserSet, AuthView, \
    ShortURLView, ResetPasswordView, ValidateEmailView, ProfileView, UserCodeSet

router = routers.SimpleRouter()
router.register(r'code-bases', CodeBaseSet)
router.register(r'code-executions', CodeExecutionSet)
router.register(r'containers', ContainerSet)
router.register(r'users', UserSet)
router.register(r'history', UserCodeSet, basename='UserCode')

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),

    path('user/profile/', ProfileView.as_view(), name='user-profile'),
    path('auth/', AuthView.as_view()),
    path('auth/validate-email/<slug:uid>/<slug:token>/', ValidateEmailView.as_view(), name='validate-email'),

    path('auth/reset-password/', ResetPasswordView.as_view(), name='init-reset-password'),
    path('auth/reset-password/<slug:uid>/<slug:token>/', ResetPasswordView.as_view(), name='reset-password'),

    path('short-url/<slug:hash>/', ShortURLView.as_view()),
]
