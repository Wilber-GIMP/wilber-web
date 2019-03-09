from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.apps import apps

from .models import *


class AssetListView(generic.ListView):
    model = Asset

class AssetFilteredListView(generic.ListView):
    model = Asset
    context_object_name = 'asset_list'
    
    def get_queryset(self):
        type = self.kwargs['type']
        queryset = Asset.objects.filter(type=type)
        return queryset

class AssetDetailView(generic.DetailView):
    model = Asset
    



class AssetCreate(generic.CreateView):
    model = Asset
    fields = ['name', 'description', 'thumbnail', 'file']
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def add_like(request, pk):
    asset = Asset.objects.get(pk=pk)
    asset.num_likes +=1
    asset.save()
    return redirect(request.META['HTTP_REFERER'])

