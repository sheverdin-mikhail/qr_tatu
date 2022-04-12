from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('qr_tatu/', views.QrTatuView.as_view(), name='qr_tatu'),
    path('for_bisnes/', views.ForBisnesView.as_view(), name='for_bisnes'),
    path('for_using/', views.ForUsingView.as_view(), name='for_using'),
    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
    path('faq/', views.FaqView.as_view(), name='faq'),
]