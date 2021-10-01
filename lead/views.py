from django.http.response import HttpResponseRedirect
from agent.mixin import OrganiserLoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.http import request
from django.urls.base import reverse
from lead.forms import (AssignedAgentForm, LeadCreateModalForm, LeadProfileForm, LeadSignUpForm, LeadUserProfileForm)
from lead.models import Agent, Lead, Profile
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView, PasswordChangeView
from lead.token import account_activation_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (DeleteView, FormView, UpdateView, CreateView) 
from django.conf import settings

class LandingPageView(TemplateView):
    template_name = 'home.html'

class LeadLoginView(LoginView):
    template_name = 'lead/login.html'
    fields = '__all__'
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('lead:lead-list')

class LeadUpdatePassword(OrganiserLoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'lead/password_change_form.html'

    def get_success_url(self):
        return reverse_lazy('lead:lead_profile', kwargs={'username':self.request.user.username})
    
    def form_valid(self, form):
        messages.success(self.request, f'Password updated successfully.')
        return super(LeadUpdatePassword, self).form_valid(form)

#ClassBaseView for Lead Signup
class LeadSignUpView(FormView):
    template_name = 'lead/register.html'
    form_class = LeadSignUpForm
    success_url = reverse_lazy('activate-sent')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            user.refresh_from_db()
            user.profile.contact = form.cleaned_data['contact']
            user.profile.gender = form.cleaned_data['gender']
            user.is_active = False
            user.save()
            #Send an activation email to the user once signup
            subject = 'Please Activate Your Account'
            use_https = self.request.is_secure(),
            current_site = get_current_site(self.request)            
            msg = render_to_string('activate.html', {
                'user': user,
                'protocol': 'https' if use_https else 'http',
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            res = send_mail(
                subject=subject, 
                message=msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[f'{user.email}'])
            if res == 1:
                redirect('activate-sent')
            else:
                messages.error(request, f'Email not sent')
        return super(LeadSignUpView, self).form_valid(form)

#Validate and Activate New Sign Lead
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        #Activate the user after clicking the link
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        messages.success(request, f'Account has been created and activated successfully!')
        return redirect('activated-complete')
    else:
        msg = messages.error(request, f'Account activated unsuccessfully!')
        return render(request, 'activation_invalid.html', {'msg':msg})     

class LeadProfileView(OrganiserLoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'lead/lead_profile.html'

    def get_object(self):
        object = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return object
        
#ClassBaseView for Profile Update
class ProfileUpdateView(OrganiserLoginRequiredMixin, UpdateView):
    model = Profile
    form_class = LeadProfileForm
    template_name = 'lead/update_profile.html'

    def get_object(self):
        object = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return object

    def get_success_url(self):
        return reverse_lazy('lead:lead_profile', kwargs={'username':self.request.user.username})
    
    def form_valid(self, form):
        messages.success(self.request, f'Account has been updated.')
        return super(ProfileUpdateView, self).form_valid(form)

#FunctionBaseView for Profile Update
class LeadUpdateProfileView(OrganiserLoginRequiredMixin, TemplateView):
    template_name = 'lead/update_profile.html'
    
    def get_success_url(self):
        return reverse_lazy('lead:lead_profile', kwargs={'username':self.request.user.username})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_profile'] = LeadProfileForm(instance=self.request.user.profile,)
        context['form_user'] = LeadUserProfileForm(instance=self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        form_profile = LeadProfileForm(instance=self.request.user.profile, data=request.POST, files=request.FILES)
        form_user = LeadUserProfileForm(instance=self.request.user, data=request.POST)
        if form_profile.is_valid() and form_user.is_valid():
            form_profile.save()
            form_user.save()
            messages.success(request, f'Account has been updated Successfully.')
        return HttpResponseRedirect(self.get_success_url())

class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'lead/lead_list.html'
    context_object_name = 'leads'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loginUser = self.request.user
        context.update({
            'unassignedLeads': Lead.objects.filter(organisation=loginUser.profile, agent__isnull=True),
        })
        return context

    def get_queryset(self):
        if self.request.user.is_organiser:
            queryset = Lead.objects.filter(organisation=self.request.user.profile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(agent__user=self.request.user)
        return queryset

class LeadCreateView(OrganiserLoginRequiredMixin, CreateView):
    form_class = LeadCreateModalForm
    template_name = 'lead/lead_create.html'
    success_url = reverse_lazy('lead:lead-list')

    def get_form_kwargs(self, **kwargs):
        kwargs = super(LeadCreateView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        user.organisation = self.request.user.profile
        user.save()
        return super(LeadCreateView, self).form_valid(form)

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'lead/lead_detail.html'
    context_object_name = 'lead'

    def get_object(self):
        object = get_object_or_404(Lead, id=self.kwargs['pk'])
        return object

class LeadUpdateView(OrganiserLoginRequiredMixin, UpdateView):
    form_class = LeadCreateModalForm
    template_name = 'lead/lead_update.html'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(LeadUpdateView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'Lead updated successfully!')
        return super(LeadUpdateView, self).form_valid(form)

    def get_object(self):
        object = get_object_or_404(Lead, id=self.kwargs['pk'])
        return object
    
    def get_success_url(self):
        return reverse('lead:lead-detail', kwargs={'pk':self.get_object().id})
    
class LeadDeleteView(OrganiserLoginRequiredMixin, DeleteView):
    template_name = 'lead/lead_delete.html'
    context_object_name = 'lead'
    success_url = reverse_lazy('lead:lead-list')

    def get_object(self):
        object = get_object_or_404(Lead, id=self.kwargs['pk'])
        return object

    def form_valid(self, form):
        messages.success(self.request, f'Lead deleted successfully!')
        return super(LeadUpdateView, self).form_valid(form)
    
class AssignedAgentFormView(OrganiserLoginRequiredMixin, FormView):
    template_name = 'lead/assigned_agent.html'
    form_class = AssignedAgentForm
    success_url = reverse_lazy('lead:lead-list')

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignedAgentFormView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs
    
    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignedAgentFormView, self).form_valid(form)
