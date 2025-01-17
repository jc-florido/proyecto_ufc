from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios_ufc
from .models import Peleadores, Pelea, Usuarios_ufc, Categoria,Evento,Noticias,Apuesta,Comentario
# Register your models here.

admin.site.register(Usuarios_ufc)
admin.site.register(Peleadores)
admin.site.register(Pelea)
admin.site.register(Categoria)
admin.site.register(Evento)
admin.site.register(Noticias)
admin.site.register(Apuesta)
admin.site.register(Comentario)

