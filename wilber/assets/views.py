from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic

from .models import *


class AssetListView(generic.ListView):
    model = Asset

class AssetDetailView(generic.DetailView):
    model = Asset


def add_like(request, pk):
    asset = Asset.objects.get(pk=pk)
    asset.num_likes +=1
    asset.save()
    return redirect(request.META['HTTP_REFERER'])

