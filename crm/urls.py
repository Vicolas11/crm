"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import template
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from lead import views
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView)

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', views.LandingPageView.as_view(), name='home'),
    path('activation_sent/', TemplateView.as_view(template_name='activate_sent.html'), name='activate-sent'),
    path('activate/<slug:uidb64>/<slug:token>', views.activate_account, name='activate'),
    path('activate/complete/', TemplateView.as_view(template_name='activated_complete.html'), name='activated-complete'),
    path('', include('agent.urls')),  
    path('', include('lead.urls')),
    path('', include('category.urls')),
    #Password Related Views
    path('lead/password-reset/', PasswordResetView.as_view(), name='password_reset_form'),
    path('lead/password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('lead/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('lead/password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

