from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.apps import apps
from django.urls import reverse_lazy

from .models import *


class AssetListView(generic.ListView):
    model = Asset

    paginate_by = 24


    def get_queryset(self, *args, **kwargs):
        #queryset = super(AssetListView, self).get_queryset(*args, **kwargs)

        queryset = Asset.objects.select_related('owner')
        return queryset


class AssetFilteredListView(generic.ListView):
    model = Asset
    context_object_name = 'asset_list'

    paginate_by = 24

    def get_queryset(self):
        category = self.kwargs['category']
        queryset = Asset.objects.filter(category=category).select_related('owner')
        return queryset


class AssetDetailView(generic.DetailView):
    model = Asset

    def get_object(self, *args):
        object = super(AssetDetailView, self).get_object(*args)
        object.num_views += 1
        object.save()
        return object


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
