from django.contrib import admin

# Register your models here.
from .models import Peleadores, Pelea, Usuarios, Categoria,Evento,Noticias,Apuesta,Comentario

admin.site.register(Peleadores)
admin.site.register(Pelea)
admin.site.register(Usuarios)
admin.site.register(Categoria)
admin.site.register(Evento)
admin.site.register(Noticias)
admin.site.register(Apuesta)
admin.site.register(Comentario)

