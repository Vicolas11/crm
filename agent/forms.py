from django import forms
from lead.models import User
from lead.models import Agent

class AgentCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name','last_name')