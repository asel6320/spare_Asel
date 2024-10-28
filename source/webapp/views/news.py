from django.shortcuts import render
from webapp.models.news import News
from django.shortcuts import get_object_or_404


def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, "news/news_detail.html", {"news": news_item})


def news_list(request):
    news_list = News.objects.order_by("-published_at")
    a = ""
    return render(request, "news/news_list.html", {"news_list": news_list})
