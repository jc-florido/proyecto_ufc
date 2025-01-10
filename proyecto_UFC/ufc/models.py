from django.db import models

# Create your models here.
from django.db import models
from django import forms
from datetime import date

# Create your models here.
class Usuarios(models.Model):
    nombre= models.CharField(max_length=100,unique=True)
    contraseña=models.CharField(max_length=100)
    correo=models.EmailField()


    def __str__(self):
        return f"{self.nombre} - {self.contraseña} - {self.correo}"
    
class Peleadores(models.Model):
    nombre= models.CharField(max_length=100)
    apellido=models.CharField(max_length=100)
    edad=models.IntegerField(max_length=2)
    codigo= models.CharField(max_length=10,unique=True)
    fecha_inicio=models.DateField()
    categoria=models.CharField(max_length=100)
    posicion=models.CharField(max_length=100)
    record=models.CharField(max_length=100)


    def __str__(self):
        return f"{self.nombre} - {self.apellido} - {self.edad} - {self.codigo} - {self.fecha_inicio} - {self.categoria} - {self.posicion} - {self.record}"
    

class Pelea(models.Model):
    codigo=models.CharField(max_length=100)
    peleador1=models.ManyToManyField(Peleadores,related_name='Peleadores')
    peleador2=models.ManyToManyField(Peleadores,related_name='Peleadores')
    fecha=models.DateField()
    ganador=models.CharField(max_length=100)
    perdedor=models.CharField(max_length=100)
    categoria=models.CharField(max_length=100)

    def __str__(self):
        return f" {self.codigo} -{self.peleador1} - {self.peleador2} - {self.fecha} - {self.ganador} - {self.perdedor} - {self.categoria}"
    
    def clean(self):
        cleaned_data = super().clean()
        peleador1 = cleaned_data.get("peleador1")
        peleador2 = cleaned_data.get("peleador2")
        if peleador1 == peleador2:
            raise forms.ValidationError("No se puede pelear contra ti mismo")
        
        return cleaned_data
    
class Evento(models.Model):
    nombre=models.IntegerField(max_length=100,unique=True)
    fecha=models.DateField()
    lugar=models.CharField(max_length=100)
    peleas=models.ManyToManyField(Pelea)

    def __str__(self):
        return f"{self.nombre} - {self.fecha} - {self.lugar} - {self.peleas}"