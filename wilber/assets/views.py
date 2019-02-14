from django.shortcuts import render

# Create your views here.

from .models import Brush, Pattern, Asset

def home(request):
    assets = Asset.objects.all()
    return render(request, 'home.html', {'assets':assets})
