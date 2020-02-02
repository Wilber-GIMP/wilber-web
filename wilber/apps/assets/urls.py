"""wilber URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from .views import *


app_name = 'asset'

urlpatterns = [
    path('',  view=AssetListView.as_view(), name='list'),

    path('new', view=AssetCreate.as_view(), name='add'),

    #path('<int:pk>',  view=AssetDetailView.as_view(), name='detail'),

    path('view/<int:pk>', AssetDetailView.as_view(), name='detail'),
    path('view/<str:slug>', AssetDetailView.as_view(), name='detail-slug'),

    path('edit/<int:pk>', AssetUpdateView.as_view(), name='edit'),
    path('edit/<str:slug>', AssetUpdateView.as_view(), name='edit-slug'),

    path('delete/<int:pk>', AssetDeleteView.as_view(), name='delete'),
    path('delete/<str:slug>', AssetDeleteView.as_view(), name='delete-slug'),

    path('<str:category>',  view=AssetFilteredListView.as_view(), name='type'),
    ]


