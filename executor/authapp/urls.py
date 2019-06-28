from django.urls import path
from authapp.views import UserCreate, UserUpdate, UserLogin, UserLogout

app_name = 'authapp'

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('update/', UserUpdate.as_view(), name='update'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
]
