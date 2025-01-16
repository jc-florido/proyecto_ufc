from django.db import models

# Create your models here.
from django.db import models
from django import forms
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuarios_ufc(AbstractUser):
    codigo=models.CharField(max_length=100,unique=True)
    correo=models.EmailField(unique=True)


    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.username} - {self.codigo} - {self.email}"
    
class Peleadores(models.Model):
    foto=models.ImageField(upload_to='fotos/')
    nombre= models.CharField(max_length=100)
    apellido=models.CharField(max_length=100)
    edad=models.IntegerField()
    codigo= models.CharField(max_length=100,unique=True)
    fecha_inicio=models.DateField()
    categoria=models.ManyToManyField('Categoria',related_name='Peleadores')
    posicion=models.CharField(max_length=100)
    record=models.CharField(max_length=100)


    def __str__(self):
        return f"{self.foto} - {self.nombre} - {self.apellido} - {self.edad} - {self.codigo} - {self.fecha_inicio} - {self.categoria} - {self.posicion} - {self.record}"
    
    def clean_fecha_inicio(self):
        cleaned_data=super().clean()
        fecha_inicio=cleaned_data.get("fecha_inicio")
        if fecha_inicio > date.today():
            raise forms.ValidationError("La fecha no puede ser superior a la actual")
        
        return cleaned_data

class Pelea(models.Model):
    codigo=models.CharField(max_length=100,unique=True)
    peleador1=models.ForeignKey(Peleadores,on_delete=models.CASCADE,related_name='Peleador_1')
    peleador2=models.ForeignKey(Peleadores,on_delete=models.CASCADE,related_name='Peleador_2')
    fecha=models.DateField()
    asaltos=models.IntegerField()
    ganador=models.ForeignKey(Peleadores,on_delete=models.CASCADE,related_name='Ganador')
    perdedor=models.ForeignKey(Peleadores,on_delete=models.CASCADE,related_name='Perdedor')
    categoria=models.ForeignKey('Categoria',on_delete=models.CASCADE,related_name='Pelea',default='pendiente')

    def __str__(self):
        return f" {self.codigo} - {self.peleador1} - {self.peleador2} - {self.fecha} - {self.asaltos} - {self.ganador} - {self.perdedor} - {self.categoria}"
    
    def clean_fecha(self):
        cleaned_data=super().clean()
        fecha=cleaned_data.get("fecha")
        if fecha < date.today():
            raise forms.ValidationError("La fecha no puede ser menor a la actual")
        
        return cleaned_data
    
    def clean(self):
        cleaned_data=super().clean()
        ganador=cleaned_data.get("ganador")
        perdedor=cleaned_data.get("perdedor")

        if ganador == perdedor:
            raise forms.ValidationError("El ganador no puede ser el mismo que el perdedor")
        if ganador == "" or perdedor == "":
            raise forms.ValidationError("Debe seleccionar un ganador y un perdedor")
        
        return cleaned_data
    
    def clean_asaltos(self):
        cleaned_data=super().clean()
        asaltos=cleaned_data.get("asaltos")
        if asaltos == 3 or asaltos == 5:
            raise forms.ValidationError("El asalto debe ser de 3 o 5")
        
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        peleador1 = cleaned_data.get("peleador1")
        peleador2 = cleaned_data.get("peleador2")
        if peleador1 == peleador2:
            raise forms.ValidationError("No se puede pelear contra ti mismo")
        
        return cleaned_data
    
class Categoria(models.Model):
    nombre=models.CharField(max_length=100,unique=True)
    peleadores=models.ManyToManyField(Peleadores,related_name='Categoria_peleadores',blank=True,default='pendiente')

    def __str__(self):
        return f"{self.nombre} - {self.peleadores}"

    def clean_peleadores(self):
        cleaned_data = super().clean()
        peleadores = cleaned_data.get("peleadores")

        # Verifica que no se agregue el mismo peleador a la categoría más de una vez
        for peleador in peleadores.all():
            if peleadores.filter(codigo=peleador.codigo).count() > 1:
                raise forms.ValidationError("No se puede agregar el mismo peleador a la misma categoría")

        return cleaned_data
    
class Evento(models.Model):
    nombre=models.IntegerField(unique=True)
    fecha=models.DateField()
    lugar=models.CharField(max_length=100)
    descripcion=models.CharField(max_length=1000)
    peleas=models.ForeignKey(Pelea,on_delete=models.CASCADE,related_name='Peleas')

    def __str__(self):
        return f"{self.nombre} - {self.fecha} - {self.lugar} - {self.descripcion} - {self.peleas}"
    
    def clean_fecha(self):
        cleaned_data=super().clean()
        fecha=cleaned_data.get("fecha")
        if fecha < date.today():
            raise forms.ValidationError("La fecha no puede ser menor a la actual")
        
        return cleaned_data
    
class Noticias(models.Model):
    codigo=models.CharField(max_length=100,unique=True)
    titulo=models.CharField(max_length=100)
    contenido=models.TextField()
    fecha=models.DateField()
    autor=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.titulo} - {self.contenido} - {self.fecha} - {self.autor}"
    
    def clean_fecha(self):
        cleaned_data=super().clean()
        fecha=cleaned_data.get("fecha")
        if fecha < date.today():
            raise forms.ValidationError("La fecha no puede ser menor a la actual")
        
        return cleaned_data
    
class Apuesta(models.Model):
    codigo=models.CharField(max_length=100,unique=True)
    usuario=models.ManyToManyField(Usuarios_ufc,related_name='Usuarios_apuestas')
    evento=models.ForeignKey(Evento,on_delete=models.CASCADE,related_name='Evento')
    pelea=models.ForeignKey(Pelea,on_delete=models.CASCADE,related_name='Pelea')
    cantidad=models.IntegerField()
    ganador=models.CharField(max_length=100,blank=True)
    empate=models.BooleanField(default=False,blank=True)
    KO=models.BooleanField(default=False,blank=True)
    asalto=models.IntegerField(blank=True)
    fecha=models.DateField()

    def __str__(self):
        return f" {self.codigo} - {self.usuario} - {self.evento} - {self.pelea} - {self.cantidad} - {self.ganador} - {self.empate} - {self.KO} - {self.asalto} - {self.fecha}"
    
    def clean_fecha(self):
        cleaned_data=super().clean()
        fecha=cleaned_data.get("fecha")
        if fecha < date.today():
            raise forms.ValidationError("La fecha no puede ser menor a la actual")
        
        return cleaned_data
    
    def clean_asalto(self):
        cleaned_data=super().clean()
        asalto=cleaned_data.get("asalto")
        if asalto < 1 or asalto > 5:
            raise forms.ValidationError("El asalto no puede ser menor a 1 ni mayor a 5")
        
        return cleaned_data
    
    def clean(self):
        cleaned_data = super().clean()
        ganador = cleaned_data.get("ganador")
        empate = cleaned_data.get("empate")

        if ganador == "" and empate == False:
            raise forms.ValidationError("Debe seleccionar un ganador o empate")
        if ganador != "" and empate == True:
            raise forms.ValidationError("No puede seleccionar un ganador y empate al mismo tiempo")
        
        return cleaned_data
    
class Comentario(models.Model):
    codigo=models.CharField(max_length=100,unique=True)
    usuario=models.ManyToManyField(Usuarios_ufc,related_name='Usuarios_comentarios')
    noticia=models.ForeignKey(Noticias,on_delete=models.CASCADE,related_name='Noticias')
    contenido=models.CharField(max_length=1000)
    fecha=models.DateField()

    def __str__(self):
        return f"{self.codigo} - {self.usuario} - {self.noticia} - {self.contenido} - {self.fecha}"
    
    def clean_fecha(self):
        cleaned_data=super().clean()
        fecha=cleaned_data.get("fecha")
        if fecha < date.today():
            raise forms.ValidationError("La fecha no puede ser menor a la actual")
        
        return cleaned_data