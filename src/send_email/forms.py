from django import forms
from .models import MailingListMember

class EmailForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)

class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingListMember
        fields = ['email']
