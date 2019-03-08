from django.shortcuts import render
from django.views import generic

from django.db.models import Sum
from django.urls import reverse_lazy

from django.contrib.auth import logout

from allauth.account.views import SignupView as AccountSignupView

# Create your views here.

from .models import *
from .forms import UserCreationForm


class UserDetailView(generic.DetailView):
    model = UserProfile
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user__username=self.kwargs['username'])
        
        
class UserMyProfileView(generic.DetailView):
    model = UserProfile
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super(UserMyProfileView, self).get_context_data(**kwargs)
        
        context['asset_list']= self.object.user.assets.all()
        context['filesize__sum']= self.object.user.assets.all().aggregate(Sum('filesize'))['filesize__sum']
        
        #ModelName.objects.filter(field_name__isnull=True).aggregate(Sum('field_name'))
        return context

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class UserEditView(generic.edit.UpdateView):
    model = UserProfile
    context_object_name = 'profile'
    
    fields = ['photo', 'phone', 'bio', 'organization', 'website', 'facebook', 'instagram', 'birthday', 'city', 'country']

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)



class SignupView(AccountSignupView):
    success_url = reverse_lazy('users:edit')

