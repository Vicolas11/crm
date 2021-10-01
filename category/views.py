from lead.models import Lead
from agent.mixin import OrganiserLoginRequiredMixin
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class CategoryListView(OrganiserLoginRequiredMixin, ListView):
    model = Lead
    template_name = 'category/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loginUser = self.request.user
        context.update({ 
            'UnassignedLeadCount': Lead.objects.filter(
                organisation=loginUser.profile, 
                category__name='Unassigned').count(),
            'ContactedLeadCount': Lead.objects.filter(
                organisation=loginUser.profile, 
                category__name='Contacted').count(),
            'ConvertedLeadCount': Lead.objects.filter(
                organisation=loginUser.profile, 
                category__name='Converted').count(),
        })
        return context
    

class CategoryContactedListView(OrganiserLoginRequiredMixin, ListView):
    model = Lead
    template_name = 'category/contact_lead.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loginUser = self.request.user
        context.update({
            'ContactedLeads': Lead.objects.filter(
                organisation=loginUser.profile, 
                category__name='Contacted'),
        })
        return context

class CategoryUnassignedListView(OrganiserLoginRequiredMixin, ListView):
    model = Lead
    template_name = 'category/unassigned_lead.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loginUser = self.request.user
        context.update({
            'UnassignedLeads': Lead.objects.filter(
                organisation=loginUser.profile, 
                category__name='Unassigned'),
        })
        return context

class CategoryConvertedListView(OrganiserLoginRequiredMixin, ListView):
    model = Lead
    template_name = 'category/converted_lead.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loginUser = self.request.user
        context.update({
            'ConvertedLeads': Lead.objects.filter(
                organisation=loginUser.profile, 
                category__name='Converted'),
        })
        return context


