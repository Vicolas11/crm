from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView
from agent.mixin import AgentLoginRequiredMixin, OrganiserLoginRequiredMixin
from agent.forms import AgentCreateForm
from lead.forms import LeadProfileForm, LeadUserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls.base import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from lead.models import Agent, Profile
from django.contrib import messages
import random
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

class AgentLoginView(LoginView):
    template_name = 'agent/login.html'
    fields = '__all__'
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('lead:lead-list')

class AgentProfileView(DetailView):
    model = Profile
    template_name = 'agent/agent_profile.html'

    def get_object(self):
        object = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return object
        
#Update Password for Agent
class AgentUpdatePassword(AgentLoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'agent/password_change_form.html'

    def get_success_url(self):
        return reverse_lazy('agent:agent_profile', kwargs={'username':self.request.user.username})
    
    def form_valid(self, form):
        messages.success(self.request, f'Password updated successfully.')
        return super(AgentUpdatePassword, self).form_valid(form)

#Agent Profile Update
class AgentUpdateProfileView(AgentLoginRequiredMixin, TemplateView):
    template_name = 'agent/agent_profile_update.html'
    
    def get_success_url(self):
        return reverse_lazy('agent:agent_profile', kwargs={'username':self.request.user.username})
    
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
    
class AgentListView(OrganiserLoginRequiredMixin, ListView):
    template_name = 'agent/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        queryset = Agent.objects.filter(organisation=self.request.user.profile)
        return queryset

class AgentCreateView(OrganiserLoginRequiredMixin, CreateView):
    form_class = AgentCreateForm
    template_name = 'agent/agent_create.html'
    success_url = reverse_lazy('agent:agent-list')

    def form_valid(self, form):
        password = random.randint(1,10000)
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f'{password}')
        user.save()
        Agent.objects.create(
            user = user,
            organisation = self.request.user.profile,
        )
        subject = 'You are invited as an agent'
        msg = f'Login details:\n{user.username}\n{password}\nAnd then reset the password.'
        send_mail(
            subject=subject, 
            message=msg,
            from_email=f'{self.request.user.email}',
            recipient_list=[f'{user.email}'])  
        messages.success(self.request, f'Agent create successfully!\nCheck {user.email} for login details.')      
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganiserLoginRequiredMixin, DetailView):
    template_name = 'agent/agent_detail.html'
    context_object_name = 'agent'

    def get_object(self):
        object = get_object_or_404(Agent, id=self.kwargs['pk'])
        return object

class AgentUpdateView(OrganiserLoginRequiredMixin, UpdateView):
    fields = ('user',)
    context_object_name = 'agent'
    template_name = 'agent/agent_update.html'

    def form_valid(self, form):
        messages.success(self.request, f'agent updated successfully!')
        return super(AgentUpdateView, self).form_valid(form)

    def get_object(self):
        object = get_object_or_404(Agent, id=self.kwargs['pk'])
        return object
    
    def get_success_url(self):
        return reverse('agent:agent-detail', kwargs={'pk':self.get_object().id})
    
class AgentDeleteView(OrganiserLoginRequiredMixin, DeleteView):
    template_name = 'agent/agent_delete.html'
    context_object_name = 'agent'
    success_url = reverse_lazy('agent:agent-list')

    def get_object(self):
        object = get_object_or_404(Agent, id=self.kwargs['pk'])
        return object

    def form_valid(self, form):
        messages.success(self.request, f'agent deleted successfully!')
        return super(AgentUpdateView, self).form_valid(form)
