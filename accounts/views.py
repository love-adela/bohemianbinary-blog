from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django import forms

from .forms import CreateUserForm


class AccountCreateView(generic.edit.CreateView):
    template_name = 'accounts/signup.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('login')

    # def post(self, request):
    #     redirect_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    #     signup_form = UserCreationForm(request.POST)
    #     if signup_form.is_valid():
    #         user = signup_form.save()
    #         auth_login(request, user)
    #         return redirect(redirect_url)
    #     return render(request, 'accounts/signup.html',
    #  {'signup_form':signup_form})

    # def get(self, request):
    #     signup_form = UserCreationForm()
    #     return render(request, 'accounts/signup.html',
    #  {'signup_form':signup_form})


# class LoginCreateView(generic.edit.CreateView):
#     success_url = '/'

#     def post(self, request):
#         redirect_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
#         login_form = AuthenticationForm(request, request.POST)
#         if login_form.is_valid():
#             auth_login(request, login_form.get_user())
#             return redirect(redirect_url)
#         return render(request, 'accounts/login.html',
#  {'login_form': login_form})

#     def get(self, request):
#         login_form = AuthenticationForm()
#         return render(request, 'accounts/login.html',
#  {'login_form': login_form})

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
