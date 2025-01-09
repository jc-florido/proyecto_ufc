from django import forms

from .models import Peleadores

from datetime import date

class PeleadoresForm(forms.ModelForm):
    class Meta:
        model = Peleadores
        fields = '__all__'
        widgets = {'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                   'fecha_fin': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),}
