from django.shortcuts import get_object_or_404,render,redirect
from .forms import CursoForm,EstudianteForm,InscripcionForm
from .models import Curso,Estudiante,Inscripcion

# Create your views here.
def principal(request):
    return render(request,'ufc/principal.html')