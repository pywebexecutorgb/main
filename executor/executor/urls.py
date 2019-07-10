from django.conf import settings
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from mainapp.views import ShortURLRedirect

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('mainapp:index'),
                                  permanent=False)),
    path('code/', include('mainapp.urls', namespace='mainapp')),
    path('auth/', include('authapp.urls', namespace='authapp')),
    path('api/', include('api.urls', namespace='api')),
    path('s/<slug:link>', ShortURLRedirect.as_view(), name='short_link'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
