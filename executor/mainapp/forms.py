import django.forms as forms

from mainapp.models import CodeBase


class CodeBaseForm(forms.ModelForm):
    class Meta:
        model = CodeBase
        exclude = ('created_at', )
        widgets = {
            'code_text': forms.Textarea({'class': 'form-control'}),
            'dependencies': forms.Textarea({'rows': 3, 'class': 'form-control'}),
            'interpreter': forms.Select({'class': 'form-control'})
        }
