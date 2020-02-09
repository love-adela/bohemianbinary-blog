from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns= [
    path('signup/', views.AccountCreateView.as_view(), name='signup'),
    path('login/', auth_views.LoginCreateView.as_view(), name='login'),
    path('logout/', auth_views.LogoutRedirectView.as_view(), name='logout')
]