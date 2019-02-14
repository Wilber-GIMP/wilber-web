from django.shortcuts import render

# Create your views here.

from .models import Brush, Pattern

def home(request):
    brushes = Brush.objects.all()
    patterns = Pattern.objects.all()
    return render(request, 'home.html', {'brushes':brushes, 'patterns':patterns})
