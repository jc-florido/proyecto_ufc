from django import forms

from .models import Peleadores, Pelea, Usuarios_ufc, Categoria,Evento,Noticias,Apuesta,Comentario

from datetime import date

class PeleadoresForm(forms.ModelForm):
    class Meta:
        model = Peleadores
        fields = '__all__'
        widgets = {'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                   'fecha_fin': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                   'record': forms.TextInput(attrs={
                            'class': 'form-control',
                            'placeholder': 'Ejemplo: 18-0-0',
                            'maxlength': '6',  # Limitar a 6 caracteres
                            'pattern': r'\d{3}-\d{3}-\d{3}',  # Validación en HTML5
                            'title': 'Debe ser del formato NN-N-N (ejemplo: 18-0-0).'}),
                    }


class ApuestaForm(forms.ModelForm):
    class Meta:
        model = Apuesta
        fields = '__all__'
        widgets = {'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                   'fecha_fin': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),}
        
        def clean(self):
            cleaned_data=super().clean()
            evento=cleaned_data.get('evento')
            pelea=cleaned_data.get('ganador')

            if evento:
                peleas=Pelea.objects.filter(evento=evento)

                if not peleas.exists():
                    raise forms.ValidationError("No hay peleas para este evento")
                
                self.fields['pelea'].queryset=peleas

            if pelea:
                ganador=Peleadores.objects.filter(pelea=pelea)
                if not ganador.exists():
                    raise forms.ValidationError("No hay ganador para esta pelea")
                
                self.fields['ganador'].queryset=ganador

            
            return cleaned_data