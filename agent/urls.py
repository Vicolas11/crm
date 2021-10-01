from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'agent'
urlpatterns = [
    path('agent/login/', views.AgentLoginView.as_view(), name='agent-login'),
    path('agent/logout/', LogoutView.as_view(next_page='home'), name='agent-logout'),
    path('agent/change-password/', views.AgentUpdatePassword.as_view(), name='password_change_done'),
    path('agent/profile/<str:username>/', views.AgentProfileView.as_view(), name='agent_profile'),
    path('agent/profile/<str:username>/update/', views.AgentUpdateProfileView.as_view(), name='update-profile'),  
    path('agent/', views.AgentListView.as_view(), name='agent-list'),
    path('agent/create/', views.AgentCreateView.as_view(), name='agent-create'), 
    path('agent/<int:pk>/detail/', views.AgentDetailView.as_view(), name='agent-detail'), 
    path('agent/<int:pk>/update/', views.AgentUpdateView.as_view(), name='agent-update'), 
    path('agent/<int:pk>/delete/', views.AgentDeleteView.as_view(), name='agent-delete'),  
]