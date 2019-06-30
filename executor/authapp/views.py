from django.shortcuts import render
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from executor import settings
from authapp.tokens import TokenGenerator
from authapp.models import PyWebUser
from authapp.forms import PyWebUserRegisterForm, PyWebUserUpdateForm, PyWebUserLoginForm


class UserCreate(CreateView):
    model = PyWebUser
    form_class = PyWebUserRegisterForm
    template_name = 'authapp/register_form.html'
    success_url = reverse_lazy('mainapp:index')
    extra_context = {'page_title': 'Register | Python webExecutor'}

    def form_valid(self, form):
        form.instance.is_active = False
        self.object = form.save()
        send_verify_email(self.object)
        return super().form_valid(form)


class UserUpdate(LoginRequiredMixin, FormView):
    model = PyWebUser
    form_class = PyWebUserUpdateForm
    template_name = 'authapp/update_form.html'
    success_url = reverse_lazy('mainapp:index')
    extra_context = {'page_title': 'Profile | Python webExecutor'}


class UserLogin(LoginView):
    form_class = PyWebUserLoginForm
    template_name = 'authapp/login_form.html'
    extra_context = {'page_title': 'Login | Python webExecutor'}

    def get_redirect_url(self):
        return reverse_lazy('mainapp:index')


class UserLogout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('mainapp:index')
    extra_context = {'page_title': 'Logout | Python webExecutor'}


def send_verify_email(user):
    subject = f'Please activate your account on {settings.DOMAIN_NAME}'
    message = render_to_string('authapp/email_verification_email.html', {
        'domain': settings.DOMAIN_NAME,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': TokenGenerator().make_token(user),
    })
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = PyWebUser.objects.get(pk=uid)
    except Exception as e:
        print(f'{e}')
        user = None
    if user and TokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        page_title = 'Verification complete | Python webExecutor'
        return render(request, 'authapp/email_verification_complete.html', context={'page_title': page_title})
    else:
        page_title = 'Verification failed | Python webExecutor'
        return render(request, 'authapp/email_verification_failed.html', context={'page_title': page_title})


class UserPasswordChange(PasswordChangeView):
    template_name = 'authapp/password_change_form.html'
    success_url = reverse_lazy('authapp:password_change_done')
    extra_context = {'page_title': 'Password change | Python webExecutor'}


class UserPasswordChangeDone(PasswordChangeDoneView):
    template_name = 'authapp/password_change_done.html'
    extra_context = {'page_title': 'Password change | Python webExecutor'}


class UserPasswordReset(PasswordResetView):
    template_name = 'authapp/password_reset_form.html'
    email_template_name = 'authapp/password_reset_email.html'
    success_url = reverse_lazy('authapp:password_reset_done')
    from_email = settings.EMAIL_HOST_USER
    extra_context = {'page_title': 'Password change | Python webExecutor'}


class UserPasswordResetDone(PasswordResetDoneView):
    template_name = 'authapp/password_reset_done.html'
    extra_context = {'page_title': 'Password reset | Python webExecutor'}


class UserPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'authapp/password_reset_confirm.html'
    success_url = reverse_lazy('authapp:password_reset_complete')
    extra_context = {'page_title': 'Password reset confirmation | Python webExecutor'}


class UserPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'authapp/password_reset_complete.html'
    extra_context = {'page_title': 'Password reset | Python webExecutor'}
