from mysite import settings
from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns= [
    path('signup/', views.AccountCreateView.as_view(), name='signup'),
    path('login/', views.LoginCreateView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]