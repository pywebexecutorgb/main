from django.urls import path

from mainapp.views import CodeCreate, CodeRead, code_read_ajax

app_name = 'mainapp'
urlpatterns = [
    path('create/', CodeCreate.as_view(), name='index'),
    path('read/<int:pk>', CodeRead.as_view(), name='read'),
    path('ajax_read/<int:pk>', code_read_ajax, name='ajax_read'),
]
