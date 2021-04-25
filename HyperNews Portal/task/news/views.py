import json

from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse, HttpResponseNotFound
from hypernews import settings

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Coming soon')


class ArticleView(View):
    def get(self, request, article_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        article = list(filter(lambda x: x['link'] == int(article_id), data))
        if not article:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        return render(request, 'article.html', context={'article': article[0]})
