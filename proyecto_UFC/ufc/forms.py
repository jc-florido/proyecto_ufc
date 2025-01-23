from django import forms

from .models import Peleadores, Pelea, Usuarios_ufc, Categoria,Evento,Noticias,Apuesta,Comentario

from datetime import date

class PeleadoresForm(forms.ModelForm):
    class Meta:
        model = Peleadores
        fields = '__all__'
        widgets = {'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                   'record': forms.TextInput(attrs={
                            'class': 'form-control',
                            'placeholder': 'Ejemplo: 18-0-0',
                            'maxlength': '6',  # Limitar a 6 caracteres
                            'pattern': r'\d{3}-\d{3}-\d{3}',  # Validación en HTML5
                            'title': 'Debe ser del formato NN-NN-NN (ejemplo: 18-0-0).'}),
                    }
        def clean(self):
            cleaned_data=super().clean()
            posicion=cleaned_data.get('posicion')
            peso=cleaned_data.get('peso')

            if posicion:
                if posicion and not (posicion == 'c' or posicion.isdigit()):
                    raise forms.ValidationError("La posición debe ser un número o la letra c")
            
            if peso:
                if peso<36:
                    raise forms.ValidationError("El peso no puede ser menor a 36")
                 


class ApuestaForm(forms.ModelForm):
    class Meta:
        model = Apuesta
        fields = '__all__'
        widgets = {'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),}
        
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
        

class PeleaForm(forms.ModelForm):
    class Meta:
        model = Pelea
        fields = '__all__'
        widgets = {'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),}
        
        def clean(self):
            cleaned_data=super().clean()
            ganador=cleaned_data.get('ganador')
            perdedor=cleaned_data.get('perdedor')

            if ganador == perdedor:
                raise forms.ValidationError("Debe seleccionar un ganador y un perdedor.")
            
            asaltos=cleaned_data.get('asaltos')
            if asaltos not in [3, 5]:
                raise forms.ValidationError("El número de asaltos debe ser 3 o 5.")
            
            return cleaned_data
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {'peleadores': forms.SelectMultiple(attrs={'size': '15'}),
                   }
        
        def clean_peleadores(self):
            cleaned_data=super().clean()
            peleadores=cleaned_data.get('peleadores')
            # Verifica que no se agregue el mismo peleador a la categoría más de una vez
            for peleador in peleadores.all():
                if peleadores.filter(codigo=peleador.codigo).count() > 1:
                    raise forms.ValidationError("No se puede agregar el mismo peleador a la misma categoría")
            
            return peleadores
        
class EventoForm(forms.ModelForm):
   class Meta:
        model = Evento
        fields = '__all__'
        widgets = {'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),}
    
        def clean(self):
            cleaned_data=super().clean()
            peleas=cleaned_data.get('peleas')
            fecha=cleaned_data.get('fecha')
            
            for pelea in peleas.all():
                if pelea.fecha != fecha and peleas.filter(codigo=pelea.codigo).count() > 1:
                    raise forms.ValidationError("No se puede agregar la misma pelea al mismo evento más de una vez y no puede tener fechas diferentes") 