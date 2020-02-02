from django.shortcuts import render
from django.views import generic
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages


from allauth.account.views import SignupView as AccountSignupView

# Create your views here.

from .models import *
from .forms import UserCreationForm


class UserDetailView(generic.DetailView):
    model = UserProfile
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user__username=self.kwargs['username'])


class UserMyProfileView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('user:detail', kwargs={'username': self.request.user.username})



class UserEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = UserProfile
    context_object_name = 'profile'

    fields = ['photo', 'phone', 'bio', 'organization', 'website', 'facebook', 'instagram', 'birthday', 'city', 'country']

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)



class SignupView(AccountSignupView):
    success_url = reverse_lazy('users:edit')

