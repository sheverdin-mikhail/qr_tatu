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
    path('change_info/', views.ChangeInfo.as_view(), name='change_info'),
    path('add_qr/', views.AddQr.as_view(), name='add_qr'),
    path('add_user_link/', views.AddUserLink.as_view(), name='add_user_link'),
    path('qr_redirect/<slug:slug>/', views.QrRedirect.as_view(), name='qr_redirect'),
    path('set_link/<slug:qr_link>/<slug:link>', views.SetLink.as_view(), name='set_link'),
    path('delete_link/<slug:link>', views.DeleteLink.as_view(), name='delete_link'),
    path('download_qr/', views.DownloadQr.as_view(), name='download_qr'),
    path('change_sub/<int:sub_id>/', views.ChangeSub.as_view(), name='change_sub'),

]
