from django.urls import path, include
from rest_framework import routers

from api.views import CodeBaseSet, CodeExecutionSet

router = routers.DefaultRouter()
router.register(r'code-base', CodeBaseSet)
router.register(r'code-execution', CodeExecutionSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
