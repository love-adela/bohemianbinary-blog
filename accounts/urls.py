from django.conf import settings
from django.urls import path

from . import views

urlpatterns= [
    path('signup/', views.AccountCreateView.as_view(), name='signup'),
    path('login/', views.LoginCreateView.as_view(), name='login'),
    path('logout/', views.LogoutRedirectView.as_view(), name='logout')
]