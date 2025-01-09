from django.db import models

# Create your models here.
from django.db import models
from django import forms
from datetime import date

# Create your models here.
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