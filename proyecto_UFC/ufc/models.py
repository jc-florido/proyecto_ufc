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
        if self.fecha_inicio > date.today():
            raise ValidationError("La fecha no puede ser superior a la actual")



class Pelea(models.Model):
    codigo=models.CharField(max_length=100,unique=True)
    foto=models.ImageField(upload_to='fotos/')
    fecha=models.DateField()
    asaltos=models.IntegerField()
    ganador=models.ForeignKey(Peleadores,on_delete=models.CASCADE,related_name='Ganador')
    perdedor=models.ForeignKey(Peleadores,on_delete=models.CASCADE,related_name='Perdedor')
    categoria=models.ForeignKey('Categoria',on_delete=models.CASCADE,related_name='Pelea',default='pendiente')

    def __str__(self):
        return f" {self.codigo} - {self.foto} - {self.fecha} - {self.asaltos} - {self.ganador} - {self.perdedor} - {self.categoria}"


    def clean(self):
        # Validación de fecha
        if self.fecha < date.today():
            raise ValidationError("La fecha no puede ser menor a la actual.")

        # Validación de peleadores
        if self.peleador1 == self.peleador2:
            raise ValidationError("No se puede pelear contra uno mismo.")

        # Validación de ganador y perdedor
        if self.ganador == self.perdedor:
            raise ValidationError("El ganador no puede ser el mismo que el perdedor.")
        if not self.ganador or not self.perdedor:
            raise ValidationError("Debe seleccionar un ganador y un perdedor.")

        # Validación de asaltos
        if self.asaltos not in [3, 5]:
            raise ValidationError("El número de asaltos debe ser 3 o 5.")

        
    
class Categoria(models.Model):
    nombre=models.CharField(max_length=100,unique=True)
    peleadores=models.ManyToManyField(Peleadores,related_name='Categoria_peleadores',blank=True,default='pendiente')

    def __str__(self):
        return f"{self.nombre} - {self.peleadores}"

    def clean_peleadores(self):
        # Verifica que no se agregue el mismo peleador a la categoría más de una vez
        for peleador in self.peleadores.all():
            if self.peleadores.filter(codigo=peleador.codigo).count() > 1:
                raise forms.ValidationError("No se puede agregar el mismo peleador a la misma categoría")

    
class Evento(models.Model):
    nombre=models.IntegerField(unique=True)
    foto=models.ImageField(upload_to='fotos/')
    fecha=models.DateField()
    lugar=models.CharField(max_length=100)
    descripcion=models.CharField(max_length=1000)
    peleas=models.ManyToManyField(Pelea,related_name='Evento_peleas',blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.foto} - {self.fecha} - {self.lugar} - {self.descripcion} - {self.peleas}"
    
    def clean_fecha(self):
        if self.fecha < date.today():
            raise ValidationError("La fecha no puede ser menor a la actual")
        
        return self.fecha
    
class Noticias(models.Model):
    codigo=models.CharField(max_length=100,unique=True)
    foto=models.ImageField(upload_to='fotos/')
    titulo=models.CharField(max_length=100)
    contenido=models.TextField()
    fecha=models.DateField()
    autor=models.ForeignKey(Usuarios_ufc,on_delete=models.CASCADE,related_name='Autor_usuario')
    def __str__(self):
        return f"{self.codigo} - {self.foto} - {self.titulo} - {self.contenido} - {self.fecha} - {self.autor}"
    
    def clean_fecha(self):
        if self.fecha < date.today():
            raise ValidationError("La fecha no puede ser menor a la actual")
        
        return self.fecha
    
class Apuesta(models.Model):
    codigo=models.CharField(max_length=100,unique=True)
    usuario=models.ManyToManyField(Usuarios_ufc,related_name='Usuarios_apuestas')
    evento=models.ForeignKey(Evento,on_delete=models.CASCADE,related_name='Evento')
    pelea=models.ForeignKey(Pelea,on_delete=models.CASCADE,related_name='Pelea')
    cantidad=models.IntegerField()
    ganador=models.ForeignKey(Peleadores,on_delete=models.CASCADE,related_name='Apuesta_Ganador',blank=True)
    empate=models.BooleanField(default=False,blank=True)
    KO=models.BooleanField(default=False,blank=True)
    asalto=models.IntegerField(blank=True)
    fecha=models.DateField()

    def __str__(self):
        return f" {self.codigo} - {self.usuario} - {self.evento} - {self.pelea} - {self.cantidad} - {self.ganador} - {self.empate} - {self.KO} - {self.asalto} - {self.fecha}"
    
    def clean_fecha(self):
        
        if self.fecha < date.today():
            raise ValidationError("La fecha no puede ser menor a la actual")
        
        if self.asalto < 1 or self.asalto > 5:
            raise ValidationError("El asalto no puede ser menor a 1 ni mayor a 5")
        
        if self.ganador == "" and self.empate == False:
            raise ValidationError("Debe seleccionar un ganador o empate")
        if self.ganador != "" and self.empate == True:
            raise ValidationError("No puede seleccionar un ganador y empate al mismo tiempo")
        
        if self.cantidad < 0:
            raise ValidationError("La cantidad no puede ser menor a 0")
        

    
    
class Comentario(models.Model):
    codigo=models.CharField(max_length=100,unique=True)
    usuario=models.ManyToManyField(Usuarios_ufc,related_name='Usuarios_comentarios')
    noticia=models.ForeignKey(Noticias,on_delete=models.CASCADE,related_name='Noticias')
    contenido=models.CharField(max_length=1000)
    fecha=models.DateField()

    def __str__(self):
        return f"{self.codigo} - {self.usuario} - {self.noticia} - {self.contenido} - {self.fecha}"
    
    def clean_fecha(self):
        if self.fecha < date.today():
            raise ValidationError("La fecha no puede ser menor a la actual")
        
