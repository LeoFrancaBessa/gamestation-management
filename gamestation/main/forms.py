from django import forms
from .models import Sessao

class SessaoForm(forms.ModelForm):
    class Meta:
        model = Sessao
        fields = ['tv', 'cliente', 'tempo_segundo']