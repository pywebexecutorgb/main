from django.conf import settings

from django.http import HttpResponse
from django.urls import path, include
from django.conf.urls.static import static

from mainapp.views import ShortURLRedirect


def http_204_no_content(*args, **kwargs):
    return HttpResponse(status=204)


urlpatterns = [
    path("api/", include("api.urls", namespace="api")),
    path("s/<slug:link>", ShortURLRedirect.as_view(), name="short_link"),
    path(
        "user/validate-email/<slug:uid>/<slug:token>/",
        http_204_no_content,
        name="validate-email",
    ),
    path(
        "user/reset-password/<slug:uid>/<slug:token>/",
        http_204_no_content,
        name="reset-password",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
