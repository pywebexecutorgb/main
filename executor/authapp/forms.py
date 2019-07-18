from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm
from authapp.models import PyWebUser


class PyWebUserRegisterForm(UserCreationForm):
    class Meta:
        model = PyWebUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class PyWebUserUpdateForm(UserChangeForm):
    class Meta:
        model = PyWebUser
        fields = (
            'email',
            'userphoto',
            'age',
            'gender',
            'country',
            'state',
            'city',
            'zipcode',
            'company',
            'bio',
            'socials',
            'proglangs',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class PyWebUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
