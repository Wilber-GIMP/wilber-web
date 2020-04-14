from allauth.account.views import SignupView as AccountSignupView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import RedirectView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.users.models import UserProfile
from apps.users.serializers import UserSerializer


class UserDetailView(generic.DetailView):
    model = UserProfile
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user__username=self.kwargs["username"])


class UserMyProfileView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            "user:detail", kwargs={"username": self.request.user.username}
        )


class UserEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = UserProfile
    context_object_name = "profile"

    fields = [
        "photo",
        "phone",
        "bio",
        "organization",
        "website",
        "facebook",
        "instagram",
        "birthday",
        "city",
        "country",
    ]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class SignupView(AccountSignupView):
    success_url = reverse_lazy("users:edit")


@api_view(["GET"])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)
