from django.conf import settings
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.conf.urls.static import static

from mainapp.views import ShortURLRedirect

urlpatterns = [
    path('', TemplateView.as_view(template_name='mainapp/index.html'), name='index'),
    path('code/<int:pk>', TemplateView.as_view(template_name='mainapp/index.html'), name='code'),
    path('user/create', TemplateView.as_view(template_name='mainapp/index.html'), name='user'),

    path('user/validate-email/<slug:uid>/<slug:token>/',
         TemplateView.as_view(template_name='mainapp/index.html'), name='validate-email'),
    path('user/reset-password/<slug:uid>/<slug:token>/',
         TemplateView.as_view(template_name='mainapp/index.html'), name='reset-password'),

    path('api/', include('api.urls', namespace='api')),
    path('s/<slug:link>', ShortURLRedirect.as_view(), name='short_link'),

    path('auth/', include('authapp.urls', namespace='authapp')),
    # path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
