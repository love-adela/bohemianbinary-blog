from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateUserForm


class AccountCreateView(generic.edit.CreateView):
    template_name = 'accounts/signup.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return to_return


class UserLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'accounts/login.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)

    def get_redirect_url(self):
        url = super().get_redirect_url()
        if url == reverse_lazy('login') or url == reverse_lazy('signup'):
            return ''
        else:
            return url
