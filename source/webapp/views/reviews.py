from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from part.models import Part
from webapp.models import Review

class CreateReviewView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        part = get_object_or_404(Part, pk=pk)

        # Проверяем, был ли запрос отправлен через AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            text = request.POST.get('text')

            if text:
                # Создаем новый отзыв
                review = Review.objects.create(
                    user=request.user,
                    part=part,
                    text=text
                )
                # Возвращаем данные в формате JSON
                return JsonResponse({
                    'success': True,
                    'username': review.user.username,
                    'text': review.text,
                })
            else:
                # Если текст отзыва пустой
                return JsonResponse({'success': False, 'error': 'Отзыв не может быть пустым'})

        return JsonResponse({'success': False, 'error': 'Неверный запрос'})
