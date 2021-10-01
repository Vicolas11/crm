from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'lead'
urlpatterns = [
    path('lead/login/', views.LeadLoginView.as_view(), name='lead-login'),
    path('lead/logout/', LogoutView.as_view(next_page='home'), name='lead-logout'),
    path('lead/signup/', views.LeadSignUpView.as_view(), name='lead-signup'),
    path('lead/change-password/', views.LeadUpdatePassword.as_view(), name='password_change_done'),
    path('lead/profile/<str:username>/', views.LeadProfileView.as_view(), name='lead_profile'),
    path('lead/profile/<str:username>/update/', views.LeadUpdateProfileView.as_view(), name='update-profile'),  
    path('lead/', views.LeadListView.as_view(), name='lead-list'),
    path('lead/create/', views.LeadCreateView.as_view(), name='lead-create'), 
    path('lead/<int:pk>/detail/', views.LeadDetailView.as_view(), name='lead-detail'), 
    path('lead/<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead-update'), 
    path('lead/<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead-delete'),
    path('lead/<int:pk>/assigned-agent/', views.AssignedAgentFormView.as_view(), name='assigned-agent'),
]