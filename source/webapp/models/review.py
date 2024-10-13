from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Review(models.Model):
    part = models.ForeignKey('webapp.Part', related_name='reviews', on_delete=models.CASCADE,
                             verbose_name='Запчасть')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Пользователь",
                             default=1)
    text = models.TextField(max_length=400, verbose_name='Отзыв')

    def __str__(self):
        return self.text[:20]

    class Meta:
        db_table = "reviews"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
