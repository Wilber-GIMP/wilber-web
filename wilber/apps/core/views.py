from django.shortcuts import render
from django.views.generic import FormView

from .forms import ReportIssueForm

# Create your views here.
class ReportIssue(FormView):
    form_class = ReportIssueForm
    template_name = 'pages/report.html'
    success_url = '.'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email(form.cleaned_data)
        return super().form_valid(form)


class ContactView(FormView):
    template_name = 'contact.html'
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)