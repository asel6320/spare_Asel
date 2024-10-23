from django.shortcuts import render
from django.views.generic import ListView

from webapp.models.news import News
from django.shortcuts import get_object_or_404


class LatestNewsView(ListView):
    model = News
    template_name = 'news/latest_news.html'
    context_object_name = 'latest'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest'] = News.objects.order_by('-published_at')[:5]
        return context


def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news/news_detail.html', {'news': news_item})


def news_list(request):
    news_list = News.objects.order_by("-published_at")
    return render(request, 'news/news_list.html', {'news_list': news_list})
