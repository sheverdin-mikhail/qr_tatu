import re

from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import authenticate, login, views, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.conf import settings
from random import choice
from qr_code.views import serve_qr_code_image

from .forms import RegisterForm, LoginForm, PersonalInfoForm, AddLinkForm, CustomPasswordResetForm
from .utils import send_email_for_verify
from .models import User, Subscription, QrCode, UserLinks

User = get_user_model()


class VerifyEmailConfirm(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        token = token_generator.check_token(user, token)
        free_sub = Subscription.objects.filter(free_sub=True).first()
        if user is not None and token:
            user.email_verify = True
            user.subscription = free_sub
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

        subs = Subscription.objects.all().order_by('id')
        user = request.user
        subscription = Subscription.objects.get(pk=user.subscription.pk)
        # qr_codes = QrCode.objects.all()
        qr_codes = (
            QrCode.objects
            .select_related('link_active')
            .filter(user=user)
            .prefetch_related('link_list')
        )
        form = PersonalInfoForm(instance=user)
        add_link_form = AddLinkForm

        context = {
            'user': user,
            'form': form,
            'qr_codes': qr_codes,
            'subscription': subscription,
            'subs': subs,
            'add_link_form': add_link_form
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


class ChangeInfo(View):
    def post(self, request):
        form = PersonalInfoForm(data=request.POST or None)
        info = request.user
        if form.is_valid():
            info.first_name = form.cleaned_data.get('first_name')
            info.last_name = form.cleaned_data.get('last_name')
            info.surname = form.cleaned_data.get('surname')
            info.phone = form.cleaned_data.get('phone')
            info.save()
        return redirect('personal')


class AddQr(View):
    def get(self, request):
        user = request.user
        subscription = Subscription.objects.get(pk=user.subscription.pk)
        qr_codes = QrCode.objects.filter(user=user).prefetch_related('link_list', 'link_active')
        if qr_codes.count() < subscription.qr_count or subscription.qr_count == 0:
            template = 'abcdefghijklmnopqrstuvwxyz0123456789'
            while True:
                qr_link = ''.join(choice(template) for i in range(7))
                qr_exists = QrCode.objects.filter(qr_link=qr_link).exists()
                if not qr_exists:
                    qr_code = QrCode(
                        qr_link=qr_link,
                        user=user
                    )
                    qr_code.save()
                    return redirect('personal')

        user = User.objects.get(pk=request.user.pk)
        form = PersonalInfoForm(instance=user)
        subs = Subscription.objects.all().order_by('id')
        add_error = f'Превышен лимит QR кодов вашей подписки. Максимальное количество кодов {subscription.qr_count}'
        context = {
            'user': user,
            'form': form,
            'qr_codes': qr_codes,
            'subs': subs,
            'add_error': add_error,
            'subscription': subscription,
        }
        return render(request, 'personal/lk.html', context)


class AddUserLink(View):
    def post(self, request):

        user = request.user
        subscription = Subscription.objects.get(pk=user.subscription.pk)
        qr_codes = QrCode.objects.filter(user=user).prefetch_related('link_list', 'link_active')
        form = PersonalInfoForm(instance=user)
        subs = Subscription.objects.all().order_by('id')
        add_error = f'Превышен лимит доступных ссылок.'
        qr = QrCode.objects.get(pk=request.POST['qr_pk'])

        add_link_form = AddLinkForm(data=request.POST or None)
        if add_link_form.is_valid():
            if subscription.link_count > qr.link_list.count() or subscription.link_count == 0:
                user_link = UserLinks(
                    link=add_link_form.cleaned_data['link'],
                    button_text=add_link_form.cleaned_data['button_text'],
                )
                user_link.save()
                qr.link_list.add(user_link)
                qr.save()
                return redirect('personal')

        context = {
            'user': user,
            'form': form,
            'qr_codes': qr_codes,
            'subs': subs,
            'add_error': add_error,
            'subscription': subscription,
        }

        return render(request, 'personal/lk.html', context)


class QrRedirect(View):

    def get(self, request, *args, **kwargs):
        qr_link = kwargs['slug']
        qr_code = QrCode.objects.get(qr_link=qr_link)
        if qr_code.link_active:
            link = qr_code.link_active.link
            return redirect(link)
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')


class SetLink(View):

    def get(self, request, *args, **kwargs):
        qr = QrCode.objects.get(qr_link=kwargs['qr_link'])
        link = UserLinks.objects.get(pk=kwargs['link'])
        qr.link_active = link
        qr.save()
        return redirect('personal')


class DeleteLink(View):

    def get(self, request, *args, **kwargs):
        link = UserLinks.objects.get(pk=kwargs['link'])
        try:
            qr_active = QrCode.objects.get(link_active__pk=link.pk)
            qr_active.link_active = None
            qr_active.save()
            link.delete()
        except ObjectDoesNotExist:
            link.delete()

        return redirect('personal')


class DownloadQr(View):

    def get(self, request):
        response = serve_qr_code_image(request)
        response['Content-Disposition'] = "attachment; filename=qr.png"
        return response


class ChangeSub(View):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        user.save_sub(kwargs['sub_id'])
        return redirect('personal')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'main/index.html'
    email_template_name = 'personal/password_reset_email.html'
    form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/index.html'
    title = 'Заявка на сброс пароля'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/index.html'
    title = 'Смена пароля'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.validlink:
    #         context['validlink'] = True
    #     else:
    #         context.update({
    #             'form': None,
    #             'title': _('Password reset unsuccessful'),
    #             'validlink': False,
    #         })
    #     return context


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/index.html'
    title = 'Успешная смена пароля'
