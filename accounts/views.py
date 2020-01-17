from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

import logging


class AccountCreateView(generic.edit.CreateView):
    def post(self, request):
        redirect_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect(redirect_url) 
        return render(request, 'accounts/signup.html', {'signup_form':signup_form})

    def get(self, request):
        signup_form = UserCreationForm()
        return render(request, 'accounts/signup.html', {'signup_form':signup_form})


class LoginCreateView(generic.edit.CreateView):
    def post(self, request):
        redirect_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(redirect_url)
        return render(request, 'accounts/login.html', {'login_form': login_form})

    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'login_form': login_form})


class LogoutRedirectView(LoginRequiredMixin, generic.base.RedirectView):
    permanent = False
    url = '/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutRedirectView, self).get(request, *args, **kwargs)
