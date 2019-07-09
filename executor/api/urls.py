from django.urls import path, include
from rest_framework import routers

from api.views import CodeBaseSet, CodeExecutionSet, ContainerSet

router = routers.SimpleRouter()
router.register(r'code-bases', CodeBaseSet)
router.register(r'code-executions', CodeExecutionSet)
router.register(r'containers', ContainerSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
