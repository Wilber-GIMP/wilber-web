from django.urls import path

from apps.users.views import UserDetailView
from apps.users.views import UserEditView
from apps.users.views import UserMyProfileView

app_name = "users"

urlpatterns = [
    path("myself", view=UserMyProfileView.as_view(), name="myself"),
    path("myself/edit", view=UserEditView.as_view(), name="edit"),
    path("<str:username>", view=UserDetailView.as_view(), name="detail"),
]
