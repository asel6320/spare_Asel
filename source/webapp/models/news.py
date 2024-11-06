from django.db import models
from django.utils.html import format_html


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    short_description = models.TextField(verbose_name="Краткое описание")
    full_text = models.TextField(verbose_name="Полный текст")
    image = models.ImageField(upload_to='news_images/', verbose_name="Изображение", blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def to_display(self):
        return [
                self.title[:30],
                self.short_description[:20],
                self.published_at,
            ]

    def get_column_headers(self):
        return [
            'Заголовок',
            'Описание',
            'Год выпуска',
        ]
