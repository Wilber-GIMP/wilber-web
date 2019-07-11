from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.apps import apps
from django.urls import reverse_lazy

from .models import *


class AssetListView(generic.ListView):
    model = Asset


class AssetFilteredListView(generic.ListView):
    model = Asset
    context_object_name = 'asset_list'

    def get_queryset(self):
        category = self.kwargs['category']
        queryset = Asset.objects.filter(category=category)
        return queryset


class AssetDetailView(generic.DetailView):
    model = Asset


class AssetUpdateView(generic.UpdateView):
    model = Asset
    fields = ['name', 'description', 'image', 'file', 'source']

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(owner=owner)

class AssetDeleteView(generic.DeleteView):
    model = Asset

    success_url = reverse_lazy('asset:list')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(owner=owner)


class AssetCreate(generic.CreateView):
    model = Asset
    fields = ['name', 'description', 'image', 'file', 'source']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
