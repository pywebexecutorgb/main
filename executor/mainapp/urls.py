from django.urls import path

from mainapp.views import CodeCreate, CodeRead

app_name = 'mainapp'
urlpatterns = [
    path('create/', CodeCreate.as_view(), name='index'),
    path('read/<int:pk>', CodeRead.as_view(), name='read'),
]
