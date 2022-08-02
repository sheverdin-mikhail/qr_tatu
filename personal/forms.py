from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm, PasswordResetForm
)
from django.core.exceptions import ValidationError
from django import forms
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import User, UserLinks
from .utils import send_email_for_verify


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')


class LoginForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            if not self.user_cache.email_verify:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Email not verify. Check your email.',
                    code='invalid login',
                )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'surname', 'first_name', 'last_name']


class AddLinkForm(forms.ModelForm):
    class Meta:
        model = UserLinks
        fields = ('link', 'button_text')


class CustomPasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMessage to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMessage(subject, body, from_email, [to_email])
        email_message.content_subtype = 'html'
        email_message.send()
