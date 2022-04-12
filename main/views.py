from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request):
        context = {}
        return render(request, 'main/index.html', context)

class QrTatuView(View):

    def get(self, request):
        context = {}
        return render(request, 'main/qr_tatu.html', context)

class ForBisnesView(View):

    def get(self, request):
        context = {}
        return render(request, 'main/for_bisnes.html', context)

class ForUsingView(View):

    def get(self, request):
        context = {}
        return render(request, 'main/for_using.html', context)

class SubscriptionView(View):

    def get(self, request):
        context = {}
        return render(request, 'main/subscription.html', context)

class FaqView(View):

    def get(self, request):
        context = {}
        return render(request, 'main/faq.html', context)