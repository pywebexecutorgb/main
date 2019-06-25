from django import forms
from .models import CodeBase


class CodeBaseForm(forms.ModelForm):
    class Meta:
        model = CodeBase
        exclude = ('created_at',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
