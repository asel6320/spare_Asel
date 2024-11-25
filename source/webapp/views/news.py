from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
import json

from webapp.models.news import News


def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, "news/news_detail.html", {"news": news_item})


def news_list(request):
    news = News.objects.order_by("-published_at")
    return render(request, "news/news_list.html", {"news_list": news})

def edit_news(request, news_id):
    news_item = get_object_or_404(News, id=news_id)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            full_text = data.get('full_text')
            short_description = data.get('short_description')
            title = data.get('title')
            image = data.get('image')
            if full_text:
                news_item.full_text = full_text
                news_item.save()
                return JsonResponse({"success": True, "message": "Новость обновлена успешно!"})
            else:
                return JsonResponse({"success": False, "message": "Ошибка: Текст отсутствует."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Ошибка: Невалидный JSON."}, status=400)
    return JsonResponse({"success": False, "message": "Метод не поддерживается."}, status=405)