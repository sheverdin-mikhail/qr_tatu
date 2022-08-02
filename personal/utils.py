import re
from email.mime.text import MIMEText

from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string, get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.conf import settings


def send_email_for_verify(request, user, use_https=False):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
        'protocol': 'https' if use_https else 'http',
    }

    # message = get_template('personal/verify_email.html').render(context)
    message = render_to_string(
        'personal/verify_email.html',
        context=context
    )
    email = EmailMessage(
        'Verify email',
        message,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()


def get_icon_template(url):
    if re.search(r't.me.', url):
        link_icon = 'tg'
    elif re.search(r'telegram.org.', url):
        link_icon = 'tg'
    elif re.search(r'instagram', url):
        link_icon = 'inst'
    elif re.search(r"vk.com", url):
        link_icon = 'vk'
    elif re.search(r"facebook.com", url):
        link_icon = 'facebook'
    elif re.search(r"gosuslugi.ru", url):
        link_icon = 'gos'
    elif re.search(r"my.mail.ru", url):
        link_icon = 'mail_ru'
    elif re.search(r"mail.ru", url):
        link_icon = 'mail_ru'
    elif re.search(r"odnoklassniki.ru", url):
        link_icon = 'ok'
    elif re.search(r"ok.ru", url):
        link_icon = 'ok'
    elif re.search(r"youtube.com", url):
        link_icon = 'youtube'
    elif re.search(r"tiktok.com", url):
        link_icon = 'tiktok'
    elif re.search(r"twitter.com", url):
        link_icon = 'twitter'
    elif re.search(r"whatsapp.com", url):
        link_icon = 'whatsapp'
    elif re.search(r"viber.com", url):
        link_icon = 'viber'
    elif re.search(r"rossgram.ru", url):
        link_icon = 'rossgram'
    elif re.search(r"rutube.ru", url):
        link_icon = 'rutube'
    elif re.search(r"tinder.com", url):
        link_icon = 'tinder'
    elif re.search(r"pinterest.ru", url):
        link_icon = 'pinterest'
    elif re.search(r"twitch.tv", url):
        link_icon = 'twitch'
    elif re.search(r"likee.video", url):
        link_icon = 'likee_video'
    elif re.search(r"linkedin.com", url):
        link_icon = 'linkedin'
    elif re.search(r"wechat.com", url):
        link_icon = 'wechat'
    elif re.search(r"snapchat.com", url):
        link_icon = 'snapchat'
    elif re.search(r"clubhouse.com", url):
        link_icon = 'clubhouse'
    else:
        link_icon = 'other'
    return link_icon
