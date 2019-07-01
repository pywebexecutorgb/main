from django.urls import path
import authapp.views as views

app_name = 'authapp'

urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='register'),
    path('update/', views.UserUpdate.as_view(), name='update'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),

    path('verify/<slug:uidb64>/<slug:token>/', views.verify, name='verify'),

    path('password_change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password_change_done/', views.UserPasswordChangeDone.as_view(), name='password_change_done'),

    path('password_reset/', views.UserPasswordReset.as_view(), name='password_reset'),
    path('password_reset_done/', views.UserPasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', views.UserPasswordResetConfirm.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/', views.UserPasswordResetComplete.as_view(), name='password_reset_complete'),
]
