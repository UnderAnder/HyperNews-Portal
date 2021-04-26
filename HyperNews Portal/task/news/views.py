from collections import defaultdict
from datetime import datetime
from json import load
from random import randrange

from django.http.response import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from hypernews import settings


with open(settings.NEWS_JSON_PATH, 'r') as json_file:
    data = load(json_file)
group_by_date = defaultdict(list)
for i in data:
    group_by_date[i['created'].split()[0]].append(i)


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news')


class ArticleView(View):
    def get(self, request, article_id, *args, **kwargs):
        article = list(filter(lambda x: x['link'] == article_id, data))
        if not article:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        return render(request, 'article.html', context={'article': article[0]})


class NewsView(View):
    def get(self, request, *args, **kwargs):
        if search := request.GET.get('q'):
            filtered = defaultdict(list)
            for k in group_by_date.keys():
                for v in group_by_date[k]:
                    if search.lower() in v['title'].lower():
                        filtered[k].append(v)
            news = dict(sorted(filtered.items(), reverse=True))
        else:
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
