import json
from random import randrange
from datetime import datetime
from collections import defaultdict
from django.shortcuts import render, redirect
from django.views import View
from django.http.response import HttpResponse, HttpResponseNotFound
from hypernews import settings


with open(settings.NEWS_JSON_PATH, 'r') as json_file:
    data = json.load(json_file)
group_by_date = defaultdict(list)
for i in data:
    group_by_date[i['created'].split()[0]].append(i)


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

        news = dict(sorted(group_by_date.items(), reverse=True))
        return render(request, 'news.html', context={'news': news})


class AddArticleView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_article.html')

    def post(self, request, *args, **kwargs):
        time = datetime.now()
        article = {"created": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "text": request.POST.get('text'),
                   "title": request.POST.get('title'),
                   "link": randrange(9999999)}
        group_by_date[time.strftime('%Y-%m-%d')].append(article)
        return redirect('/news')
