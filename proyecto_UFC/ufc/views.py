from django.shortcuts import get_object_or_404,render,redirect
from .forms import PeleadoresForm
from .models import Peleadores

# Create your views here.
def principal(request):
    return render(request,'paginas/principal.html')