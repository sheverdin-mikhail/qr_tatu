from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import View
from django.contrib.auth.forms import AuthenticationForm

from .mixins import *
from personal.forms import RegisterForm, LoginForm


class IndexView(FromsMixin, View):

    def get(self, request):
        register_form = RegisterForm()
        login_form = LoginForm()

        context = {
            'register_form': register_form,
            'form': login_form
        }
        print(request.user)
        return render(request, 'main/index.html', context)


class QrTatuView(View):

    def get(self, request):
        register_form = RegisterForm()
        login_form = LoginForm()

        context = {
            'register_form': register_form,
            'form': login_form
        }
        return render(request, 'main/qr_tatu.html', context)


class ForBisnesView(View):

    def get(self, request):
        register_form = RegisterForm()
        login_form = LoginForm()

        context = {
            'register_form': register_form,
            'form': login_form
        }
        return render(request, 'main/for_bisnes.html', context)


class ForUsingView(View):

    def get(self, request):
        register_form = RegisterForm()
        login_form = LoginForm()

        context = {
            'register_form': register_form,
            'form': login_form
        }
        return render(request, 'main/for_using.html', context)


class SubscriptionView(View):

    def get(self, request):
        register_form = RegisterForm()
        login_form = LoginForm()

        context = {
            'register_form': register_form,
            'form': login_form
        }
        return render(request, 'main/subscription.html', context)


class FaqView(View):

    def get(self, request):
        register_form = RegisterForm()
        login_form = LoginForm()

        context = {
            'register_form': register_form,
            'form': login_form
        }
        return render(request, 'main/faq.html', context)

