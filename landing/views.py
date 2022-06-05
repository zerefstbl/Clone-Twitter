from django.shortcuts import render

from django.views import View

from django.contrib.auth.models import User


class Index(View):
    def get(self, request, *args, **kwargs):

        usuarios = User.objects.all().order_by('-id')

        context = {'usuarios': usuarios}

        return render(request, 'landing/index.html', context)

    def post(self, request, *args, **kwargs):

        usuarios = User.objects.all().order_by('-id')

        context = {'usuarios': usuarios}

        return render(request, 'landing/index.html', context)
