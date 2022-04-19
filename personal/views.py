from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import authenticate, login, views, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.conf import settings

from .forms import RegisterForm, LoginForm
from .utils import send_email_for_verify

User = get_user_model()


class VerifyEmailConfirm(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        token = token_generator.check_token(user, token)

        if user is not None and token:
            user.email_verify = True
            user.save()
            login(request, user)
            return HttpResponseRedirect('/lk')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


class PersonalCabinet(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        context = {

        }

        return render(request, 'personal/lk.html', context)


class PersonalRegister(View):

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            register_form.save()
            email = register_form.cleaned_data.get('email')
            password = register_form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('verify_email')
        return HttpResponseRedirect('/lk')


class PersonalLogin(LoginView):
    form_class = LoginForm
    template_name = 'main/index.html'


