
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
      
class OrganiserLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organiser"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organiser:
            return redirect('lead:lead-list')
        return super().dispatch(request, *args, **kwargs)

class AgentLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an agent"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_agent:
            return redirect('lead:lead-login')
        return super().dispatch(request, *args, **kwargs)
