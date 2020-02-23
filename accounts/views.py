from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateUserForm


class AccountCreateView(generic.edit.CreateView):
    template_name = 'accounts/signup.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('login')


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
