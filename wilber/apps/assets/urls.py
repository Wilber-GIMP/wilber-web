from django.urls import path

from apps.assets.views import AssetCreate
from apps.assets.views import AssetDeleteView
from apps.assets.views import AssetDetailView
from apps.assets.views import AssetFilteredListView
from apps.assets.views import AssetListView
from apps.assets.views import AssetUpdateView
from apps.assets.views import MyAssetListView


app_name = "asset"

urlpatterns = [
    path("", view=AssetListView.as_view(), name="list"),
    path("my", view=MyAssetListView.as_view(), name="myself"),
    path("new", view=AssetCreate.as_view(), name="add"),
    # path('<int:pk>',  view=AssetDetailView.as_view(), name='detail'),
    path("view/<int:pk>", AssetDetailView.as_view(), name="detail"),
    path("view/<str:slug>", AssetDetailView.as_view(), name="detail-slug"),
    path("edit/<int:pk>", AssetUpdateView.as_view(), name="edit"),
    path("edit/<str:slug>", AssetUpdateView.as_view(), name="edit-slug"),
    path("delete/<int:pk>", AssetDeleteView.as_view(), name="delete"),
    path("delete/<str:slug>", AssetDeleteView.as_view(), name="delete-slug"),
    path("<str:category>", view=AssetFilteredListView.as_view(), name="type"),
]
