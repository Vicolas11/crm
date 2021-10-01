from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'category'
urlpatterns = [ 
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/unassigned-lead/', views.CategoryUnassignedListView.as_view(), name='unassigned-lead'),
    path('category/converted-lead/', views.CategoryConvertedListView.as_view(), name='converted-lead'),
    path('category/contacted-lead/', views.CategoryContactedListView.as_view(), name='contacted-lead'),
]