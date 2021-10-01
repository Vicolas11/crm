from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import *

admin.site.register(Category)

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','gender','contact','avatar',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_organiser','is_agent',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    list_display = ('id','email','username','first_name', 'last_name', 'is_staff',)
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('-id',)

 
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('user','gender','contact','avatar','signup_confirmation')}),
    )
    list_display = ('id','user','gender','contact','avatar','signup_confirmation',)
    search_fields = ('id','user',)
    ordering = ('-id',)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('first_name','last_name','age','email','contact','description','date_created','agent','category','organisation',)}),
    )
    list_display = ('id','first_name','last_name','age','email','contact','description','agent','category','organisation',)
    search_fields = ('id','level', 'first_name', 'last_name',)
    ordering = ('-id',)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('user','date_created','organisation')}),
    )
    list_display = ('id','user','date_created','organisation')
    search_fields = ('id','user',)
    ordering = ('-id',)
