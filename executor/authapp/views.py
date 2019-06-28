from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from authapp.models import PyWebUser
from authapp.forms import PyWebUserRegisterForm, PyWebUserUpdateForm, PyWebUserLoginForm


class UserCreate(CreateView):
    model = PyWebUser
    form_class = PyWebUserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('mainapp:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Register | Python webExecutor'
        return context


@method_decorator(login_required(), name='dispatch')
class UserUpdate(FormView):
    model = PyWebUser
    form_class = PyWebUserUpdateForm
    template_name = 'authapp/update.html'
    success_url = reverse_lazy('mainapp:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Profile | Python webExecutor'
        return context


class UserLogin(LoginView):
    form_class = PyWebUserLoginForm
    template_name = 'authapp/login.html'
    success_url = reverse_lazy('mainapp:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login | Python webExecutor'
        return context

    def get_redirect_url(self):
        return reverse_lazy('mainapp:index')


@method_decorator(login_required(), name='dispatch')
class UserLogout(LogoutView):
    next_page = reverse_lazy('mainapp:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Logout | Python webExecutor'
        return context
