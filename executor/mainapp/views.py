from django.urls import reverse
from django.views.generic import RedirectView

from mainapp.utils import ShortURL


class ShortURLRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        link = self.kwargs.get("link")
        codebase_pk = ShortURL().decode(link)
        return reverse("code", kwargs={"pk": codebase_pk})
