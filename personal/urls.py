from django.urls import path
from django.views.generic import TemplateView
from personal import views

urlpatterns = [
    path('signup/', views.PersonalRegister.as_view(), name='signup'),
    path('login/', views.PersonalLogin.as_view(), name='login'),
    path('verify_email/',
         TemplateView.as_view(template_name='personal/confirm_email.html'),
         name='verify_email'
         ),
    path('verify_email_confirm/<uidb64>/<token>/', views.VerifyEmailConfirm.as_view(),
         name='verify_email_confirm'
         ),
    path('invalid_verify/', TemplateView.as_view(template_name='personal/invalid_verify.html'),
         name='invalid_verify'
         ),
    path('lk/', views.PersonalCabinet.as_view(),
         name='personal'
         ),
]
