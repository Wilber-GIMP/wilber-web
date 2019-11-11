from django import forms


class ReportIssueForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self, data):
        # send email using the self.cleaned_data dictionary
        print("SEND", data)