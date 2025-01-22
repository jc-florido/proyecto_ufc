from django.shortcuts import get_object_or_404,render,redirect
from .forms import PeleadoresForm
from .models import Peleadores, Pelea, Usuarios_ufc, Categoria,Evento,Noticias,Apuesta,Comentario

# Create your views here.
def principal(request):
    eventos=Evento.objects.all()
    noticias=Noticias.objects.all()
    apuestas=Apuesta.objects.all()
    comentarios=Comentario.objects.all()
    return render (request, 'paginas/principal.html', {'eventos':eventos,'noticias':noticias,'apuestas':apuestas,'comentarios':comentarios})

def logout(request):
    return render(request, 'paginas/logout.html')