from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Coming soon')
