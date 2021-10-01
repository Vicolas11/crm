from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Agent, Lead, User
from django.forms import forms
from django import forms
from .models import Profile

class LeadCreateModalForm(forms.ModelForm):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none(), empty_label='No Agent', required=False)

    class Meta:
        model = Lead
        exclude = ('organisation',)   
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(LeadCreateModalForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = Agent.objects.filter(organisation=request.user.profile)

class AssignedAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none(), empty_label='No Agent', required=False)

    def __init__(self, **kwargs):
        request = kwargs.pop('request')
        super(AssignedAgentForm, self).__init__(**kwargs)
        self.fields['agent'].queryset = Agent.objects.filter(organisation=request.user.profile)

class LeadProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['gender', 'contact', 'avatar']
        widgets = {
            'gender': forms.RadioSelect()
        }

class LeadUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

class LeadSignUpForm(UserCreationForm):
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    GenderChoice = (('Male','Male'), ('Female','Female'),('Others','Others'))
    contact = forms.CharField(validators = [phoneNumberRegex], max_length = 16)
    gender = forms.ChoiceField(choices=GenderChoice)

    class Meta:
        model = User
        widgets = {
            'gender': forms.RadioSelect()
        }
        fields = ['username', 'first_name', 'last_name', 
        'gender', 'contact', 'email',  'password1', 'password2',]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exit!')
        return email
    
    def save(self, commit=True):
        user = super(LeadSignUpForm, self).save(commit=False)
        user.gender = self.cleaned_data['gender']
        user.contact = self.cleaned_data['contact']        
        if commit:
            user.save()
        return user
            
