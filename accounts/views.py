from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse_lazy
from djang.views import generic


class AccountCreateView(generic.edit.CreateView):
    def post(self, request):
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            return redirect('blog/post_list')

    def get(self, request):
        signup_form = UserCreationForm()
        return render(request, 'accounts/signup.html', {'signup_form':signup_form})


# WIP: login, logout
def login(request):
    if request.mehotd == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
        return redirect('blog/post_list')
    else:
        login_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'login_form': login_form})


def logout(request):
    auth_logout(request)
    return redirect('blog/post_list')

