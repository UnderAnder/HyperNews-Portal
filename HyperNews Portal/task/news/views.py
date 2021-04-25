import json
from collections import defaultdict
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
        article = list(filter(lambda x: x['link'] == article_id, data))
        if not article:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        return render(request, 'article.html', context={'article': article[0]})


class NewsView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        group_by_date = defaultdict(list)
        for i in data:
            group_by_date[i['created'].split()[0]].append(i)
        news = dict(sorted(group_by_date.items(), reverse=True))
        return render(request, 'news.html', context={'news': news})
